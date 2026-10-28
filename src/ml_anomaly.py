"""
src/ml_anomaly.py
Hafta 3: Veri Normalizasyonu ve Makine Öğrenmesi Tabanlı Anomali Tespiti Modülü.
Harici kütüphane bağımlılığı olmadan saf Python ile:
1. Min-Max ve Z-Score Veri Normalizasyonu (DataNormalizer)
2. Isolation Forest (İzolasyon Ormanı - Liu et al., 2008) Algoritması (IsolationForestDetector)
3. k-En Yakın Komşu (k-NN) Yoğunluk / Mesafe Tabanlı Aykırı Değer Tespiti (KNNOutlierDetector)
4. İstatistiksel + Kural Bazlı + Makine Öğrenmesi Hibrit Risk Motoru (HybridAnomalyEngine)
"""
import math
import random
from typing import List, Dict, Any, Optional, Tuple

FEATURE_KEYS = [
    ("liquidity", "current_ratio"),
    ("liquidity", "acid_test_ratio"),
    ("liquidity", "cash_ratio"),
    ("leverage", "financial_leverage"),
    ("leverage", "debt_to_equity"),
    ("leverage", "equity_ratio"),
    ("profitability", "net_profit_margin"),
    ("profitability", "gross_profit_margin"),
    ("profitability", "operating_profit_margin"),
    ("profitability", "roa"),
    ("profitability", "roe"),
    ("activity", "asset_turnover"),
    ("activity", "inventory_turnover")
]


class DataNormalizer:
    """Finansal oran vektörlerini makine öğrenmesi modelleri için normalize eder."""

    @staticmethod
    def extract_feature_vector(ratios: Dict[str, Dict[str, Optional[float]]]) -> List[float]:
        """Şirketin oran sözlüğünden sabit sıralı sayısal özellik vektörü çıkarır."""
        vec = []
        for cat, metric in FEATURE_KEYS:
            val = ratios.get(cat, {}).get(metric)
            if val is None or math.isnan(val):
                vec.append(0.0)
            else:
                vec.append(float(val))
        return vec

    @staticmethod
    def min_max_normalize(matrix: List[List[float]]) -> Tuple[List[List[float]], List[Tuple[float, float]]]:
        """
        Özellik matrisini [0, 1] aralığına Min-Max yöntemiyle normalize eder.
        Sabit değerli sütunlarda (max == min) sıfıra bölünmeyi önlemek için 0.5 atar.
        """
        if not matrix:
            return [], []

        n_rows = len(matrix)
        n_cols = len(matrix[0])
        bounds: List[Tuple[float, float]] = []

        for col in range(n_cols):
            col_vals = [matrix[row][col] for row in range(n_rows)]
            c_min, c_max = min(col_vals), max(col_vals)
            bounds.append((c_min, c_max))

        normalized: List[List[float]] = []
        for row in range(n_rows):
            norm_row = []
            for col in range(n_cols):
                c_min, c_max = bounds[col]
                if abs(c_max - c_min) < 1e-9:
                    norm_row.append(0.5)
                else:
                    norm_val = (matrix[row][col] - c_min) / (c_max - c_min)
                    norm_row.append(round(norm_val, 6))
            normalized.append(norm_row)

        return normalized, bounds


def _c_factor(n: int) -> float:
    """
    Isolation Forest ortalama yol uzunluğu düzeltme faktörü c(n).
    Formül: 2 * H(n-1) - 2*(n-1)/n, burada H(i) ~= ln(i) + 0.5772156649 (Euler sabiti).
    """
    if n <= 1:
        return 0.0
    if n == 2:
        return 1.0
    euler_gamma = 0.5772156649
    h = math.log(n - 1.0) + euler_gamma
    return 2.0 * h - (2.0 * (n - 1.0) / n)


class _IsolationNode:
    """İzolasyon Ağacı düğüm yapısı."""
    def __init__(
        self,
        size: int = 0,
        split_attr: Optional[int] = None,
        split_val: Optional[float] = None,
        left: Optional['_IsolationNode'] = None,
        right: Optional['_IsolationNode'] = None,
        is_external: bool = True
    ):
        self.size = size
        self.split_attr = split_attr
        self.split_val = split_val
        self.left = left
        self.right = right
        self.is_external = is_external


class IsolationForestDetector:
    """
    Makine Öğrenmesi Tabanlı İzolasyon Ormanı (Isolation Forest) Anomali Dedektörü.
    Aykırı finansal profilleri rastgele alt-uzay bölmeleriyle izole etme hızına göre puanlar.
    """

    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.trees: List[_IsolationNode] = []
        self.n_samples: int = 0
        self.height_limit: int = 0

    def fit(self, X: List[List[float]]):
        """Veri matrisi üzerinde izolasyon ağaçlarını eğitir."""
        self.n_samples = len(X)
        if self.n_samples == 0:
            return
        self.height_limit = max(1, int(math.ceil(math.log2(max(self.n_samples, 2)))))
        rng = random.Random(self.random_state)
        self.trees = []

        for _ in range(self.n_estimators):
            tree = self._build_tree(X, current_height=0, rng=rng)
            self.trees.append(tree)

    def _build_tree(self, data: List[List[float]], current_height: int, rng: random.Random) -> _IsolationNode:
        n_samples = len(data)
        if current_height >= self.height_limit or n_samples <= 1:
            return _IsolationNode(size=n_samples, is_external=True)

        n_features = len(data[0])
        # Varyansı olan özellikleri bul
        valid_attrs = []
        for attr in range(n_features):
            vals = [row[attr] for row in data]
            if max(vals) - min(vals) > 1e-9:
                valid_attrs.append((attr, min(vals), max(vals)))

        if not valid_attrs:
            return _IsolationNode(size=n_samples, is_external=True)

        split_attr, v_min, v_max = rng.choice(valid_attrs)
        split_val = rng.uniform(v_min, v_max)

        left_data = [row for row in data if row[split_attr] < split_val]
        right_data = [row for row in data if row[split_attr] >= split_val]

        if not left_data or not right_data:
            return _IsolationNode(size=n_samples, is_external=True)

        left_node = self._build_tree(left_data, current_height + 1, rng)
        right_node = self._build_tree(right_data, current_height + 1, rng)

        return _IsolationNode(
            size=n_samples,
            split_attr=split_attr,
            split_val=split_val,
            left=left_node,
            right=right_node,
            is_external=False
        )

    def _path_length(self, x: List[float], node: _IsolationNode, current_height: int) -> float:
        if node.is_external or node.split_attr is None or node.split_val is None:
            return float(current_height) + _c_factor(node.size)

        if x[node.split_attr] < node.split_val:
            return self._path_length(x, node.left, current_height + 1)
        else:
            return self._path_length(x, node.right, current_height + 1)

    def score_samples(self, X: List[List[float]]) -> List[float]:
        """
        Her bir örnek için [0, 100] aralığında Isolation Forest anomali skoru döndürür.
        Kısa ortalama yol uzunluğu (hızlı izolasyon) -> Yüksek anomali skoru.
        """
        if not self.trees or self.n_samples <= 1:
            return [0.0 for _ in X]

        c_n = _c_factor(self.n_samples)
        if c_n <= 0:
            return [0.0 for _ in X]

        scores = []
        for x in X:
            avg_path = sum(self._path_length(x, t, 0) for t in self.trees) / len(self.trees)
            # Standart IF skoru: s = 2^(-E(h(x)) / c(n)), aralık (0, 1)
            raw_if_score = math.pow(2.0, -avg_path / c_n)
            # 0.5 civarı normal, 0.65+ belirgin anomali; 0-100 ölçeğine doğrusal olmayan kalibrasyon
            calibrated = max(0.0, min(100.0, (raw_if_score - 0.35) / 0.45 * 100.0))
            scores.append(round(calibrated, 1))
        return scores


class KNNOutlierDetector:
    """
    k-En Yakın Komşu (k-NN) Mesafe Tabanlı Aykırı Değer Dedektörü.
    Normalize uzayda bir şirketin en yakın k komşusuna olan ortalama Öklid uzaklığını ölçer.
    """

    def __init__(self, k: int = 2):
        self.k = k

    def score_samples(self, X_norm: List[List[float]]) -> List[float]:
        n = len(X_norm)
        if n <= 1:
            return [0.0 for _ in X_norm]

        k_eff = min(self.k, n - 1)
        avg_dists = []

        for i in range(n):
            dists = []
            for j in range(n):
                if i == j:
                    continue
                d = math.sqrt(sum((X_norm[i][f] - X_norm[j][f]) ** 2 for f in range(len(X_norm[i]))))
                dists.append(d)
            dists.sort()
            avg_k_dist = sum(dists[:k_eff]) / k_eff
            avg_dists.append(avg_k_dist)

        max_dist = max(avg_dists) if avg_dists else 1.0
        min_dist = min(avg_dists) if avg_dists else 0.0

        scores = []
        for d in avg_dists:
            if max_dist - min_dist < 1e-9:
                scores.append(20.0)
            else:
                # Sektördeki en uzak şirkete göre bağıl yoğunluk sapması (0-100)
                rel = ((d - min_dist) / (max_dist - min_dist)) * 85.0
                scores.append(round(rel, 1))
        return scores


class HybridAnomalyEngine:
    """
    İstatistiksel Z-Score + Kural Bazlı Finansal Eşik + Isolation Forest + k-NN
    modellerini birleştiren Hibrit Karar Destek Motoru.
    """

    def __init__(self):
        self.iforest = IsolationForestDetector(n_estimators=100, random_state=42)
        self.knn = KNNOutlierDetector(k=2)

    def analyze_all_companies(
        self,
        companies: List[Any],
        company_ratios: Dict[str, Dict[str, Dict[str, Optional[float]]]],
        base_risk_reports: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Tüm şirketler için makine öğrenmesi modellerini çalıştırır ve hibrit risk raporu üretir.
        """
        # 1. Özellik matrisini çıkar ve normalize et
        codes = [c.code for c in companies]
        raw_matrix = [DataNormalizer.extract_feature_vector(company_ratios[code]) for code in codes]
        norm_matrix, _ = DataNormalizer.min_max_normalize(raw_matrix)

        # 2. Genel ve sektörel ML skorlarını hesapla
        self.iforest.fit(norm_matrix)
        if_scores = self.iforest.score_samples(norm_matrix)
        knn_scores = self.knn.score_samples(norm_matrix)

        results: Dict[str, Dict[str, Any]] = {}
        for idx, code in enumerate(codes):
            base = base_risk_reports[code]
            stat_rule_score = float(base.get("risk_score", 0.0))
            if_score = if_scores[idx]
            knn_score = knn_scores[idx]

            # Hibrit Ağırlıklandırma:
            # %55 İstatistiksel Z-Score & Kritik İflas Kuralları
            # %30 Isolation Forest (Makine Öğrenmesi)
            # %15 k-NN Komşuluk Uzaklığı
            hybrid_score = round(
                min(100.0, max(0.0, 0.55 * stat_rule_score + 0.30 * if_score + 0.15 * knn_score)),
                1
            )

            # Eğer şirkette kritik iflas bayrağı (negatif özkaynak vb.) varsa ve kural skoru 90+ ise hibrit skoru düşürme
            if stat_rule_score >= 85.0:
                hybrid_score = max(hybrid_score, round(0.80 * stat_rule_score + 0.20 * if_score, 1))

            if hybrid_score < 25.0:
                hybrid_level = "Düşük Risk (Normal / Dengeli)"
            elif hybrid_score < 55.0:
                hybrid_level = "Orta Risk (İzlenmeli)"
            elif hybrid_score < 78.0:
                hybrid_level = "Yüksek Risk (Anomali Sinyali)"
            else:
                hybrid_level = "Kritik Risk / Yüksek Anomali"

            enriched = dict(base)
            enriched["statistical_rule_score"] = stat_rule_score
            enriched["isolation_forest_score"] = if_score
            enriched["knn_outlier_score"] = knn_score
            enriched["hybrid_risk_score"] = hybrid_score
            enriched["hybrid_risk_level"] = hybrid_level
            enriched["normalized_features"] = norm_matrix[idx]
            results[code] = enriched

        return results
