from odoo import api, fields, models
from statistics import mean, pstdev
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
import requests


class HanVietExchangeRate(models.Model):
    _name = 'hanviet.exchange.rate'
    _description = 'Han Viet KRW to VND Exchange Rate'
    _order = 'date desc'

    # ==================================================
    # System fields
    # ==================================================
    active = fields.Boolean(default=True)

    state = fields.Selection(
        [
            ('new', 'New'),
            ('fetched', 'Fetched'),
            ('analyzed', 'Analyzed'),
            ('approved', 'Approved'),
            ('archived', 'Archived'),
        ],
        default='new',
        required=True,
        copy=False
    )

    # ==================================================
    # Business fields (INPUT)
    # ==================================================
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today
    )

    krw_to_vnd = fields.Float(
        string='KRW → VND Rate',
        digits=(16, 6),
        help='Exchange rate from KRW to VND'
    )

    user_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user,
        readonly=True
    )

    # ==================================================
    # Computed fields
    # ==================================================
    sma_7 = fields.Float(
        string='SMA 7',
        compute='_compute_indicators',
        store=True
    )

    sma_30 = fields.Float(
        string='SMA 30',
        compute='_compute_indicators',
        store=True
    )

    volatility = fields.Float(
        string='Volatility',
        compute='_compute_indicators',
        store=True
    )

    recommendation = fields.Selection(
        [
            ('buy', 'Buy'),
            ('hold', 'Hold'),
            ('avoid', 'Avoid'),
        ],
        compute='_compute_recommendation',
        store=True
    )

    ema_7 = fields.Float(
        string='EMA 7',
        compute='_compute_advanced_indicators',
        store=True
    )

    ema_30 = fields.Float(
        string='EMA 30',
        compute='_compute_advanced_indicators',
        store=True
    )

    roc_7 = fields.Float(
        string='ROC 7 days',
        compute='_compute_advanced_indicators',
        store=True
    )

    trend_strength = fields.Float(
        string='Trend Strength',
        compute='_compute_advanced_indicators',
        store=True
    )

    bollinger_upper = fields.Float(
        compute='_compute_advanced_indicators',
        store=True
    )

    bollinger_lower = fields.Float(
        compute='_compute_advanced_indicators',
        store=True
    )




    # ==================================================
    # COMPUTE METHODS
    # ==================================================


    @api.depends('date')
    def _compute_indicators(self):
        """
        Compute SMA7, SMA30 and volatility
        based on historical KRW→VND rates up to selected date.
        """
        for record in self:
            domain = [
                ('date', '<=', record.date),
                ('state', 'in', ['fetched', 'analyzed', 'approved'])
            ]

            rates = self.search(
                domain,
                order='date desc',
                limit=30
            ).mapped('krw_to_vnd')

            record.sma_7 = mean(rates[:7]) if len(rates) >= 7 else 0.0
            record.sma_30 = mean(rates) if len(rates) >= 30 else 0.0
            record.volatility = pstdev(rates) if len(rates) >= 2 else 0.0

  
    def _compute_ema(self, prices, period):
        """
        Compute EMA for the latest value.
        """
        if len(prices) < period:
            return 0.0

        k = 2 / (period + 1)
        ema = prices[-period]

        for price in prices[-period + 1:]:
            ema = price * k + ema * (1 - k)

        return ema
            
    @api.depends('date', 'krw_to_vnd')
    def _compute_advanced_indicators(self):
        for record in self:
            domain = [
                ('date', '<=', record.date),
                ('state', 'in', ['fetched', 'analyzed', 'approved'])
            ]

            rates = self.search(
                domain,
                order='date asc',
                limit=30
            ).mapped('krw_to_vnd')

            if len(rates) < 7:
                record.ema_7 = 0.0
                record.ema_30 = 0.0
                record.roc_7 = 0.0
                record.trend_strength = 0.0
                record.bollinger_upper = 0.0
                record.bollinger_lower = 0.0
                continue

            # EMA
            record.ema_7 = self._compute_ema(rates, 7)
            record.ema_30 = self._compute_ema(rates, 30)

            # ROC (7 days)
            record.roc_7 = (
                (rates[-1] - rates[-7]) / rates[-7]
                if rates[-7] else 0.0
            )

            # Trend strength (slope of SMA7)
            record.trend_strength = (
                record.sma_7 - mean(rates[-14:-7])
                if len(rates) >= 14 else 0.0
            )

            # Bollinger Bands (using SMA30 + volatility)
            record.bollinger_upper = record.sma_30 + 2 * record.volatility
            record.bollinger_lower = record.sma_30 - 2 * record.volatility

    @api.depends(
        'sma_7', 'sma_30',
        'ema_7', 'ema_30',
        'roc_7', 'volatility',
        'bollinger_upper', 'bollinger_lower',
        'krw_to_vnd'
    )
    def _compute_recommendation(self):
        for record in self:
            reasons = []

            if not record.ema_7 or not record.ema_30:
                record.recommendation = 'hold'
                record.recommendation_reason = 'Not enough data for advanced analysis.'
                continue

            # High risk condition
            if record.volatility > record.sma_30 * 0.06:
                record.recommendation = 'avoid'
                reasons.append('Volatility is too high.')

            # BUY condition
            elif (
                record.ema_7 > record.ema_30 and
                record.roc_7 > 0 and
                record.krw_to_vnd < record.bollinger_upper
            ):
                record.recommendation = 'buy'
                reasons.append('EMA7 > EMA30 (uptrend).')
                reasons.append('Positive momentum (ROC > 0).')
                reasons.append('Price is below upper Bollinger Band.')

            # AVOID condition
            elif (
                record.ema_7 < record.ema_30 or
                record.krw_to_vnd > record.bollinger_upper
            ):
                record.recommendation = 'avoid'
                reasons.append('Downtrend or price overheated.')

            else:
                record.recommendation = 'hold'
                reasons.append('Mixed signals detected.')

            record.recommendation_reason = '\n'.join(reasons)

    recommendation_reason = fields.Text(
        string='Recommendation Explanation',
        compute='_compute_recommendation',
        store=True
    )

    # ==================================================
    # ACTION METHODS
    # ==================================================
    def action_fetch(self):
            """
            Fetch historical KRW → VND exchange rate
            for the selected date using System Parameter API key.
            """
            for record in self:
                if record.state != 'new':
                    raise UserError('Only records in New state can be fetched.')

                api_key = self.env['ir.config_parameter'].sudo().get_param(
                    'hanviet.exchange.api_key'
                )

                if not api_key:
                    raise UserError(
                        'API key is missing. '
                        'Please configure System Parameter: hanviet.exchange.api_key'
                    )

                url = 'https://api.exchangerate.host/historical'
                params = {
                    'access_key': api_key,
                    'date': record.date.strftime('%Y-%m-%d'),
                    'format': 1
                }

                try:
                    response = requests.get(url, params=params, timeout=15)
                    response.raise_for_status()
                    data = response.json()
                except Exception as e:
                    raise UserError(f'API connection error: {e}')

                if not data.get('success'):
                    raise UserError('API returned an error response.')

                quotes = data.get('quotes', {})
                usd_krw = quotes.get('USDKRW')
                usd_vnd = quotes.get('USDVND')

                if not usd_krw or not usd_vnd:
                    raise UserError('KRW or VND rate missing in API response.')

                # KRW → VND = USDVND / USDKRW
                record.krw_to_vnd = usd_vnd / usd_krw
                record.state = 'fetched'

            return True

    def action_analyze(self):
        for record in self:
            if record.state not in ['new', 'fetched']:
                raise UserError('Only new or fetched records can be analyzed.')

            if not record.krw_to_vnd:
                raise UserError('Exchange rate is missing.')

            record.state = 'analyzed'
        return True

    def action_approve(self):
        for record in self:
            if record.state != 'analyzed':
                raise UserError('Only analyzed records can be approved.')
            record.state = 'approved'
        return True

    def action_archive(self):
        for record in self:
            if record.state == 'approved':
                raise UserError('Approved records cannot be archived.')
            record.state = 'archived'
        return True


    # ==================================================
    # CONSTRAINTS
    # ==================================================
    _sql_constraints = [
        (
            'unique_date',
            'UNIQUE(date)',
            'Exchange rate for this date already exists.'
        ),
        (
            'check_rate_positive',
            'CHECK(krw_to_vnd > 0)',
            'Exchange rate must be positive.'
        )
    ]

    def action_approve(self):
        for record in self:
            if record.state != 'analyzed':
                raise UserError('Only analyzed records can be approved.')

            if record.sma_30:
                lower = record.sma_30 * 0.8
                upper = record.sma_30 * 1.2

                if record.krw_to_vnd < lower or record.krw_to_vnd > upper:
                    raise UserError(
                        'Exchange rate deviates more than ±20% from SMA30. '
                        'Please review before approval.'
                    )

            record.state = 'approved'
        return True
