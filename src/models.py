"""
src/models.py
Şirket, Bilanço ve Gelir Tablosu veri modelleri.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class BalanceSheet:
    # Dönen Varlıklar
    cash_and_equivalents: float     # Nakit ve Nakit Benzerleri
    accounts_receivable: float      # Ticari Alacaklar
    inventories: float              # Stoklar
    other_current_assets: float     # Diğer Dönen Varlıklar
    
    # Duran Varlıklar
    tangible_assets: float          # Maddi Duran Varlıklar
    intangible_assets: float        # Maddi Olmayan Duran Varlıklar
    other_non_current_assets: float # Diğer Duran Varlıklar

    # Kısa Vadeli Yabancı Kaynaklar (KVYK)
    short_term_financial_debt: float# Kısa Vadeli Finansal Borçlar
    short_term_trade_payables: float# Ticari Borçlar
    other_short_term_debt: float    # Diğer Kısa Vadeli Yükümlülükler

    # Uzun Vadeli Yabancı Kaynaklar (UVYK)
    long_term_financial_debt: float # Uzun Vadeli Finansal Borçlar
    other_long_term_debt: float     # Diğer Uzun Vadeli Yükümlülükler

    # Özkaynaklar
    paid_in_capital: float          # Ödenmiş Sermaye
    retained_earnings: float        # Geçmiş Yıl Kârları / Yedekler
    net_period_profit_bs: float     # Dönem Net Kârı (Bilançodaki)

    @property
    def total_current_assets(self) -> float:
        """Toplam Dönen Varlıklar"""
        return (self.cash_and_equivalents + self.accounts_receivable + 
                self.inventories + self.other_current_assets)

    @property
    def total_non_current_assets(self) -> float:
        """Toplam Duran Varlıklar"""
        return (self.tangible_assets + self.intangible_assets + 
                self.other_non_current_assets)

    @property
    def total_assets(self) -> float:
        """Toplam Varlıklar (Aktif Toplamı)"""
        return self.total_current_assets + self.total_non_current_assets

    @property
    def total_short_term_liabilities(self) -> float:
        """Toplam Kısa Vadeli Yabancı Kaynaklar"""
        return (self.short_term_financial_debt + self.short_term_trade_payables + 
                self.other_short_term_debt)

    @property
    def total_long_term_liabilities(self) -> float:
        """Toplam Uzun Vadeli Yabancı Kaynaklar"""
        return self.long_term_financial_debt + self.other_long_term_debt

    @property
    def total_liabilities(self) -> float:
        """Toplam Borç / Yabancı Kaynaklar"""
        return self.total_short_term_liabilities + self.total_long_term_liabilities

    @property
    def total_equity(self) -> float:
        """Toplam Özkaynaklar (Pasif Toplamı = Borçlar + Özkaynaklar)"""
        return self.paid_in_capital + self.retained_earnings + self.net_period_profit_bs


@dataclass
class IncomeStatement:
    net_sales: float                # Net Satışlar (Hasılat)
    cost_of_sales: float            # Satışların Maliyeti (Negatif girilebilir, mutlak değer alınır)
    operating_expenses: float       # Faaliyet Giderleri (Genel yönetim, pazarlama vb.)
    financial_expenses: float       # Finansman Giderleri
    tax_expenses: float             # Vergi Giderleri
    net_profit: float               # Net Dönem Kârı / Zararı

    @property
    def gross_profit(self) -> float:
        """Brüt Satış Kârı = Net Satışlar - Satışların Maliyeti"""
        return self.net_sales - abs(self.cost_of_sales)

    @property
    def operating_profit(self) -> float:
        """Faaliyet Kârı (EBIT/FVÖK) = Brüt Kâr - Faaliyet Giderleri"""
        return self.gross_profit - abs(self.operating_expenses)


@dataclass
class Company:
    code: str
    name: str
    sector: str
    period: str
    balance_sheet: BalanceSheet
    income_statement: IncomeStatement
    extra_info: Dict[str, Any] = field(default_factory=dict)
