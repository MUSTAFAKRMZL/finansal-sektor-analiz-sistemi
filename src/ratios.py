"""
src/ratios.py
Finansal Oran Hesaplayıcı Modülü (FinancialRatioCalculator).
Likidite, Kaldıraç/Borçluluk, Kârlılık ve Faaliyet oranlarını hesaplar.
"""
from typing import Dict, Any, Optional
from src.models import Company, BalanceSheet, IncomeStatement

def safe_divide(numerator: float, denominator: float, default: Optional[float] = None) -> Optional[float]:
    """Sıfıra bölünme ve geçersiz veri durumlarını güvenli şekilde yönetir."""
    if denominator is None or denominator == 0:
        return default
    return round(numerator / denominator, 4)

class FinancialRatioCalculator:
    """Şirketlerin finansal tablolarından standart finansal oranları hesaplar."""

    @staticmethod
    def calculate_all(company: Company) -> Dict[str, Dict[str, Optional[float]]]:
        bs = company.balance_sheet
        inc = company.income_statement

        return {
            "liquidity": FinancialRatioCalculator.calculate_liquidity_ratios(bs),
            "leverage": FinancialRatioCalculator.calculate_leverage_ratios(bs),
            "profitability": FinancialRatioCalculator.calculate_profitability_ratios(bs, inc),
            "activity": FinancialRatioCalculator.calculate_activity_ratios(bs, inc)
        }

    @staticmethod
    def calculate_liquidity_ratios(bs: BalanceSheet) -> Dict[str, Optional[float]]:
        """
        Likidite Oranları:
        Şirketin kısa vadeli borçlarını ödeme gücünü gösterir.
        """
        cur_assets = bs.total_current_assets
        short_liab = bs.total_short_term_liabilities
        inventories = bs.inventories
        cash = bs.cash_and_equivalents

        # 1. Cari Oran (Current Ratio) = Dönen Varlıklar / KVYK (İdeal: 1.5 - 2.0)
        current_ratio = safe_divide(cur_assets, short_liab)

        # 2. Asit-Test / Likit Oran = (Dönen Varlıklar - Stoklar) / KVYK (İdeal: >= 1.0)
        acid_test_ratio = safe_divide(cur_assets - inventories, short_liab)

        # 3. Nakit Oran = Nakit ve Benzerleri / KVYK (İdeal: >= 0.20)
        cash_ratio = safe_divide(cash, short_liab)

        return {
            "current_ratio": current_ratio,
            "acid_test_ratio": acid_test_ratio,
            "cash_ratio": cash_ratio
        }

    @staticmethod
    def calculate_leverage_ratios(bs: BalanceSheet) -> Dict[str, Optional[float]]:
        """
        Borçluluk / Finansal Kaldıraç Oranları:
        Varlıkların ne kadarının borçla finanse edildiğini gösterir.
        """
        total_assets = bs.total_assets
        total_debt = bs.total_liabilities
        total_equity = bs.total_equity
        short_liab = bs.total_short_term_liabilities

        # 1. Finansal Kaldıraç Oranı = Toplam Borç / Toplam Aktif (İdeal: < 0.65)
        financial_leverage = safe_divide(total_debt, total_assets)

        # 2. Borç / Özkaynak Oranı = Toplam Borç / Özkaynaklar
        debt_to_equity = safe_divide(total_debt, total_equity)

        # 3. Özkaynak Oranı = Özkaynaklar / Toplam Aktif
        equity_ratio = safe_divide(total_equity, total_assets)

        # 4. Kısa Vadeli Borç Ağırlığı = KVYK / Toplam Borç
        short_term_debt_ratio = safe_divide(short_liab, total_debt)

        return {
            "financial_leverage": financial_leverage,
            "debt_to_equity": debt_to_equity,
            "equity_ratio": equity_ratio,
            "short_term_debt_ratio": short_term_debt_ratio
        }

    @staticmethod
    def calculate_profitability_ratios(bs: BalanceSheet, inc: IncomeStatement) -> Dict[str, Optional[float]]:
        """
        Kârlılık Oranları:
        Şirketin satışları ve varlıkları üzerinden kâr üretme kapasitesini ölçer.
        """
        sales = inc.net_sales
        net_profit = inc.net_profit
        gross_profit = inc.gross_profit
        op_profit = inc.operating_profit
        total_assets = bs.total_assets
        total_equity = bs.total_equity

        # 1. Net Kâr Marjı = Net Kâr / Net Satışlar
        net_profit_margin = safe_divide(net_profit, sales)

        # 2. Brüt Kâr Marjı = Brüt Kâr / Net Satışlar
        gross_profit_margin = safe_divide(gross_profit, sales)

        # 3. Faaliyet Kâr Marjı = Faaliyet Kârı / Net Satışlar
        operating_profit_margin = safe_divide(op_profit, sales)

        # 4. Aktif Kârlılığı (ROA) = Net Kâr / Toplam Aktif
        roa = safe_divide(net_profit, total_assets)

        # 5. Özkaynak Kârlılığı (ROE) = Net Kâr / Özkaynaklar
        roe = safe_divide(net_profit, total_equity)

        return {
            "net_profit_margin": net_profit_margin,
            "gross_profit_margin": gross_profit_margin,
            "operating_profit_margin": operating_profit_margin,
            "roa": roa,
            "roe": roe
        }

    @staticmethod
    def calculate_activity_ratios(bs: BalanceSheet, inc: IncomeStatement) -> Dict[str, Optional[float]]:
        """
        Faaliyet / Devir Hızı Oranları:
        Şirketin varlıklarını ne kadar etkin ve verimli kullandığını gösterir.
        """
        sales = inc.net_sales
        total_assets = bs.total_assets
        inventories = bs.inventories
        cost_of_sales = abs(inc.cost_of_sales)

        # 1. Aktif Devir Hızı = Net Satışlar / Toplam Aktif
        asset_turnover = safe_divide(sales, total_assets)

        # 2. Stok Devir Hızı = Satışların Maliyeti / Stoklar
        inventory_turnover = safe_divide(cost_of_sales, inventories)

        return {
            "asset_turnover": asset_turnover,
            "inventory_turnover": inventory_turnover
        }
