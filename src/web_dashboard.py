"""
src/web_dashboard.py
Hafta 3: İnteraktif Görsel Analiz Ekranı (Web Dashboard) Üreticisi ve Yerel Web Sunucusu.
Şirketlerin finansal rasyolarını, sektör ortalaması/medyanı karşılaştırmalarını,
Isolation Forest + Z-Score hibrit risk puanlarını ve canlı bilanço simülatörünü
içeren bağımsız HTML5/JS/SVG görsel analiz ekranı üretir.
"""
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import List, Dict, Any
from src.models import Company

class DashboardGenerator:
    """Analiz sonuçlarını interaktif bir Web Dashboard (HTML5 + SVG Radar & Bar Grafikleri) olarak dışa aktarır."""

    @staticmethod
    def export_dashboard(
        companies: List[Company],
        sector_benchmarks: Dict[str, Any],
        company_comparisons: Dict[str, Dict[str, Any]],
        hybrid_reports: Dict[str, Dict[str, Any]],
        output_path: str = "dashboard.html"
    ) -> str:
        payload = {
            "companies": [
                {
                    "code": c.code,
                    "name": c.name,
                    "sector": c.sector,
                    "period": c.period,
                    "total_assets": c.balance_sheet.total_assets,
                    "total_liabilities": c.balance_sheet.total_liabilities,
                    "total_equity": c.balance_sheet.total_equity,
                    "net_sales": c.income_statement.net_sales,
                    "net_profit": c.income_statement.net_profit
                }
                for c in companies
            ],
            "sector_benchmarks": sector_benchmarks,
            "comparisons": company_comparisons,
            "hybrid_reports": hybrid_reports
        }

        json_payload = json.dumps(payload, ensure_ascii=False)

        html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Akıllı Finansal Performans ve Sektörel Anomali Analiz Sistemi</title>
    <style>
        :root {{
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --bg-card-hover: #263449;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-indigo: #6366f1;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --border-color: #334155;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; }}
        body {{ background-color: var(--bg-dark); color: var(--text-main); line-height: 1.5; padding-bottom: 50px; }}
        header {{
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 20px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .brand h1 {{ font-size: 1.35rem; font-weight: 700; color: var(--accent-blue); letter-spacing: 0.3px; }}
        .brand p {{ font-size: 0.85rem; color: var(--text-muted); }}
        .badge-version {{
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-blue);
            border: 1px solid rgba(56, 189, 248, 0.4);
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .container {{ max-width: 1400px; margin: 24px auto; padding: 0 24px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px 20px;
        }}
        .kpi-title {{ font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.6px; }}
        .kpi-value {{ font-size: 1.8rem; font-weight: 700; margin-top: 6px; }}
        .kpi-sub {{ font-size: 0.78rem; color: var(--text-muted); margin-top: 4px; }}

        .controls-bar {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 24px;
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }}
        .control-group {{ display: flex; flex-direction: column; gap: 6px; flex: 1; min-width: 220px; }}
        .control-group label {{ font-size: 0.8rem; color: var(--text-muted); font-weight: 600; }}
        select, input {{
            background: #0f172a;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 0.92rem;
            outline: none;
        }}
        select:focus, input:focus {{ border-color: var(--accent-blue); }}

        .dashboard-grid {{ display: grid; grid-template-columns: 1.05fr 1.35fr; gap: 20px; margin-bottom: 24px; }}
        @media (max-width: 1024px) {{ .dashboard-grid {{ grid-template-columns: 1fr; }} }}
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
            margin-bottom: 16px;
        }}
        .card-title {{ font-size: 1.02rem; font-weight: 600; color: #e2e8f0; }}

        .score-box {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }}
        .score-pill {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
        }}
        .score-pill .lbl {{ font-size: 0.75rem; color: var(--text-muted); }}
        .score-pill .val {{ font-size: 1.35rem; font-weight: 700; margin-top: 4px; }}

        .alert-list {{ margin-top: 12px; display: flex; flex-direction: column; gap: 8px; max-height: 220px; overflow-y: auto; }}
        .alert-item {{
            padding: 10px 12px;
            border-radius: 8px;
            font-size: 0.84rem;
            border-left: 4px solid;
        }}
        .alert-critical {{ background: rgba(239, 68, 68, 0.12); border-left-color: var(--accent-red); color: #fecaca; }}
        .alert-warning {{ background: rgba(245, 158, 11, 0.12); border-left-color: var(--accent-amber); color: #fde68a; }}
        .alert-ok {{ background: rgba(16, 185, 129, 0.12); border-left-color: var(--accent-green); color: #a7f3d0; }}

        table {{ width: 100%; border-collapse: collapse; font-size: 0.86rem; }}
        th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border-color); }}
        th {{ color: var(--text-muted); font-weight: 600; background: rgba(15, 23, 42, 0.5); }}
        tr:hover {{ background: var(--bg-card-hover); }}
        .tag {{ padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }}
        .tag-low {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
        .tag-med {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; }}
        .tag-high {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}

        .sim-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 16px; }}
        .btn-primary {{
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-indigo));
            color: #fff;
            border: none;
            padding: 11px 22px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.92rem;
        }}
        .btn-primary:hover {{ opacity: 0.92; }}
        .legend {{ display: flex; gap: 16px; justify-content: center; margin-top: 8px; font-size: 0.8rem; color: var(--text-muted); }}
        .legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
        .dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
    </style>
</head>
<body>

<header>
    <div class="brand">
        <h1>Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi</h1>
        <p>Yazılım Geliştirme I • Hafta 3: Veri Normalizasyonu, Isolation Forest ML Anomali Tespiti ve Görsel Analiz Ekranı</p>
    </div>
    <div class="badge-version">Sürüm v0.3.0 • Hibrit ML Motoru Aktif</div>
</header>

<div class="container">
    <!-- Üst KPI Kartları -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-title">Analiz Edilen Şirket</div>
            <div class="kpi-value" id="kpiTotalCompanies">0</div>
            <div class="kpi-sub">SQLite Veritabanında Kayıtlı</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Aktif Sektör Sayısı</div>
            <div class="kpi-value" id="kpiTotalSectors">0</div>
            <div class="kpi-sub">Dinamik Benchmark Hesaplamalı</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Ortalama Hibrit Risk</div>
            <div class="kpi-value" id="kpiAvgRisk">0.0</div>
            <div class="kpi-sub">0 - 100 Ölçeğinde (Z-Skor + ML)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Yüksek Riskli / Anomalili Şirket</div>
            <div class="kpi-value" id="kpiCriticalCount" style="color: var(--accent-red);">0</div>
            <div class="kpi-sub">Isolation Forest & Kural Tespiti</div>
        </div>
    </div>

    <!-- Filtre ve Şirket Seçim Çubuğu -->
    <div class="controls-bar">
        <div class="control-group">
            <label for="sectorSelect">Sektör Filtresi</label>
            <select id="sectorSelect" onchange="onSectorFilterChange()">
                <option value="ALL">Tüm Sektörler</option>
            </select>
        </div>
        <div class="control-group">
            <label for="companySelect">İncelenen Şirket</label>
            <select id="companySelect" onchange="renderSelectedCompany()"></select>
        </div>
    </div>

    <!-- Orta Görsel Analiz Paneli: Sol Risk & Radar, Sağ Sektör Kıyaslama Bar Grafiği -->
    <div class="dashboard-grid">
        <div class="card">
            <div class="card-header">
                <span class="card-title" id="selectedCompanyTitle">Şirket Risk & ML Anomali Profili</span>
                <span id="selectedRiskBadge" class="tag tag-low">Düşük Risk</span>
            </div>

            <div class="score-box">
                <div class="score-pill">
                    <div class="lbl">Bileşik Hibrit Risk Puanı</div>
                    <div class="val" id="valHybridScore" style="color: var(--accent-blue);">0.0 / 100</div>
                </div>
                <div class="score-pill">
                    <div class="lbl">Isolation Forest (ML) Skoru</div>
                    <div class="val" id="valIfScore" style="color: var(--accent-indigo);">0.0 / 100</div>
                </div>
                <div class="score-pill">
                    <div class="lbl">İstatistiksel & Kural Skoru</div>
                    <div class="val" id="valStatScore">0.0 / 100</div>
                </div>
                <div class="score-pill">
                    <div class="lbl">k-NN Komşuluk Sapması</div>
                    <div class="val" id="valKnnScore">0.0 / 100</div>
                </div>
            </div>

            <!-- SVG Radar Chart -->
            <div style="text-align: center; margin: 12px 0;">
                <svg id="radarSvg" width="340" height="270" viewBox="0 0 340 270"></svg>
                <div class="legend">
                    <span><i class="dot" style="background: #38bdf8;"></i> Seçili Şirket</span>
                    <span><i class="dot" style="background: #f59e0b;"></i> Sektör Ortalaması</span>
                </div>
            </div>

            <div class="card-header" style="margin-top: 12px; padding-bottom: 8px;">
                <span class="card-title" style="font-size: 0.9rem;">Tespit Edilen Anomaliler ve Finansal Uyarılar</span>
            </div>
            <div class="alert-list" id="anomalyAlertList"></div>
        </div>

        <div class="card">
            <div class="card-header">
                <span class="card-title">Sektör Ortalaması ve Medyanı ile Rasyo Karşılaştırması</span>
                <span style="font-size: 0.8rem; color: var(--text-muted);" id="sectorNameLabel"></span>
            </div>

            <!-- SVG Bar Chart -->
            <div style="margin-bottom: 18px; overflow-x: auto;">
                <svg id="barSvg" width="680" height="240" viewBox="0 0 680 240"></svg>
            </div>

            <!-- Detaylı Rasyo Tablosu -->
            <div style="max-height: 330px; overflow-y: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Kategori</th>
                            <th>Finansal Gösterge</th>
                            <th>Şirket</th>
                            <th>Sektör Ort.</th>
                            <th>Sektör Medyan</th>
                            <th>Fark (%)</th>
                            <th>Z-Skor</th>
                        </tr>
                    </thead>
                    <tbody id="ratioTableBody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Canlı Yeni Şirket Bilanço Simülatörü -->
    <div class="card" style="margin-bottom: 24px;">
        <div class="card-header">
            <span class="card-title">Canlı Bilanço & Gelir Tablosu Analiz Simülatörü (Yeni Şirket Testi)</span>
            <span style="font-size: 0.8rem; color: var(--text-muted);">Değerleri girip anlık sektör kıyaslaması ve anomali puanı üretebilirsiniz</span>
        </div>
        <div class="sim-grid">
            <div class="control-group"><label>Şirket Adı</label><input type="text" id="simName" value="Örnek Yeni Teknoloji A.Ş."></div>
            <div class="control-group"><label>Sektör</label><select id="simSector"></select></div>
            <div class="control-group"><label>Dönen Varlıklar (TL)</label><input type="number" id="simCurAssets" value="18000000"></div>
            <div class="control-group"><label>Stoklar (TL)</label><input type="number" id="simInventories" value="4000000"></div>
            <div class="control-group"><label>Nakit ve Benzerleri (TL)</label><input type="number" id="simCash" value="5000000"></div>
            <div class="control-group"><label>Toplam Varlıklar / Aktif (TL)</label><input type="number" id="simTotalAssets" value="40000000"></div>
            <div class="control-group"><label>Kısa Vadeli Borçlar (TL)</label><input type="number" id="simShortDebt" value="12000000"></div>
            <div class="control-group"><label>Toplam Borçlar (TL)</label><input type="number" id="simTotalDebt" value="22000000"></div>
            <div class="control-group"><label>Özkaynaklar (TL)</label><input type="number" id="simEquity" value="18000000"></div>
            <div class="control-group"><label>Net Satışlar (TL)</label><input type="number" id="simSales" value="50000000"></div>
            <div class="control-group"><label>Net Dönem Kârı (TL)</label><input type="number" id="simNetProfit" value="6000000"></div>
        </div>
        <div style="display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">
            <button class="btn-primary" onclick="runLiveSimulation()">Analiz Et ve Sektörle Karşılaştır</button>
            <div id="simResultBox" style="font-size: 0.92rem; color: var(--accent-blue); font-weight: 600;"></div>
        </div>
    </div>

    <!-- Tüm Şirketler Genel Sıralama Tablosu -->
    <div class="card">
        <div class="card-header">
            <span class="card-title">Tüm Şirketler Sektörel Performans ve Hibrit Anomali Sıralaması</span>
        </div>
        <div style="overflow-x: auto;">
            <table>
                <thead>
                    <tr>
                        <th>Kod</th>
                        <th>Şirket Adı</th>
                        <th>Sektör</th>
                        <th>Cari Oran</th>
                        <th>Finansal Kaldıraç</th>
                        <th>Net Kâr Marjı</th>
                        <th>ROE</th>
                        <th>İstatistik Skoru</th>
                        <th>Isolation Forest (ML)</th>
                        <th>Hibrit Risk Puanı</th>
                        <th>Risk Durumu</th>
                    </tr>
                </thead>
                <tbody id="allCompaniesTableBody"></tbody>
            </table>
        </div>
    </div>
</div>

<script>
const DATA = {json_payload};

function initDashboard() {{
    const companies = DATA.companies;
    const sectors = Object.keys(DATA.sector_benchmarks);

    document.getElementById('kpiTotalCompanies').textContent = companies.length;
    document.getElementById('kpiTotalSectors').textContent = sectors.length;

    let totalRisk = 0;
    let critCount = 0;
    companies.forEach(c => {{
        const rep = DATA.hybrid_reports[c.code];
        if (rep) {{
            totalRisk += rep.hybrid_risk_score;
            if (rep.hybrid_risk_score >= 50) critCount++;
        }}
    }});
    document.getElementById('kpiAvgRisk').textContent = (totalRisk / (companies.length || 1)).toFixed(1);
    document.getElementById('kpiCriticalCount').textContent = critCount;

    const sectorSelect = document.getElementById('sectorSelect');
    const simSector = document.getElementById('simSector');
    sectors.forEach(s => {{
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = s;
        sectorSelect.appendChild(opt);

        const opt2 = document.createElement('option');
        opt2.value = s; opt2.textContent = s;
        simSector.appendChild(opt2);
    }});

    populateCompanySelect('ALL');
    renderAllCompaniesTable();
    renderSelectedCompany();
}}

function populateCompanySelect(sectorFilter) {{
    const select = document.getElementById('companySelect');
    select.innerHTML = '';
    DATA.companies
        .filter(c => sectorFilter === 'ALL' || c.sector === sectorFilter)
        .forEach(c => {{
            const opt = document.createElement('option');
            opt.value = c.code;
            opt.textContent = `[${{c.code}}] ${{c.name}} (${{c.sector}})`;
            select.appendChild(opt);
        }});
}}

function onSectorFilterChange() {{
    const sec = document.getElementById('sectorSelect').value;
    populateCompanySelect(sec);
    renderSelectedCompany();
}}

function renderSelectedCompany() {{
    const code = document.getElementById('companySelect').value;
    if (!code) return;

    const comp = DATA.companies.find(c => c.code === code);
    const compReport = DATA.comparisons[code];
    const risk = DATA.hybrid_reports[code];

    document.getElementById('selectedCompanyTitle').textContent = `${{comp.name}} [${{comp.code}}]`;
    document.getElementById('sectorNameLabel').textContent = `Sektör: ${{comp.sector}} (${{comp.period}})`;

    document.getElementById('valHybridScore').textContent = `${{risk.hybrid_risk_score.toFixed(1)}} / 100`;
    document.getElementById('valIfScore').textContent = `${{risk.isolation_forest_score.toFixed(1)}} / 100`;
    document.getElementById('valStatScore').textContent = `${{risk.statistical_rule_score.toFixed(1)}} / 100`;
    document.getElementById('valKnnScore').textContent = `${{risk.knn_outlier_score.toFixed(1)}} / 100`;

    const badge = document.getElementById('selectedRiskBadge');
    badge.textContent = risk.hybrid_risk_level;
    badge.className = 'tag ' + (risk.hybrid_risk_score >= 55 ? 'tag-high' : (risk.hybrid_risk_score >= 25 ? 'tag-med' : 'tag-low'));

    // Uyarı listesi
    const alertList = document.getElementById('anomalyAlertList');
    alertList.innerHTML = '';
    if (risk.critical_flags.length === 0 && risk.anomalies.length === 0) {{
        alertList.innerHTML = `<div class="alert-item alert-ok">✓ Şirketin tüm finansal oranları sektör normları ile uyumludur. Anomali tespit edilmedi.</div>`;
    }} else {{
        risk.critical_flags.forEach(f => {{
            alertList.innerHTML += `<div class="alert-item alert-critical"><strong>[Kritik Eşik İhlali]</strong> ${{f}}</div>`;
        }});
        risk.anomalies.forEach(a => {{
            alertList.innerHTML += `<div class="alert-item alert-warning"><strong>[Z-Skor Sapması: ${{a.metric}}]</strong> ${{a.message}} (Z: ${{a.z_score}})</div>`;
        }});
    }}

    // Rasyo Tablosu
    const tbody = document.getElementById('ratioTableBody');
    tbody.innerHTML = '';
    compReport.comparisons.forEach(item => {{
        const cVal = item.company_value !== null ? item.company_value.toFixed(4) : '-';
        const sMean = item.sector_mean !== null ? item.sector_mean.toFixed(4) : '-';
        const sMed = item.sector_median !== null ? item.sector_median.toFixed(4) : '-';
        const diff = item.diff_percentage !== null ? (item.diff_percentage > 0 ? '+' : '') + item.diff_percentage.toFixed(1) + '%' : '-';
        const z = item.z_score !== null ? (item.z_score > 0 ? '+' : '') + item.z_score.toFixed(2) : '-';
        const zColor = (item.z_score !== null && Math.abs(item.z_score) >= 1.5) ? 'color: #f87171; font-weight: 700;' : '';

        tbody.innerHTML += `
            <tr>
                <td>${{item.category.toUpperCase()}}</td>
                <td>${{item.metric.replace(/_/g, ' ').toUpperCase()}}</td>
                <td style="font-weight: 600;">${{cVal}}</td>
                <td>${{sMean}}</td>
                <td>${{sMed}}</td>
                <td>${{diff}}</td>
                <td style="${{zColor}}">${{z}}</td>
            </tr>
        `;
    }});

    drawRadarChart(compReport.comparisons);
    drawBarChart(compReport.comparisons);
}}

function drawRadarChart(comparisons) {{
    const svg = document.getElementById('radarSvg');
    svg.innerHTML = '';
    const cx = 170, cy = 135, radius = 95;
    const metrics = [
        {{ key: 'current_ratio', label: 'Cari Oran' }},
        {{ key: 'acid_test_ratio', label: 'Asit-Test' }},
        {{ key: 'equity_ratio', label: 'Özkaynak Or.' }},
        {{ key: 'net_profit_margin', label: 'Net Kâr M.' }},
        {{ key: 'roa', label: 'ROA' }},
        {{ key: 'asset_turnover', label: 'Aktif Devir' }}
    ];

    const N = metrics.length;
    // Grid halkaları
    [0.25, 0.5, 0.75, 1.0].forEach(level => {{
        let pts = [];
        for (let i = 0; i < N; i++) {{
            const angle = (Math.PI * 2 * i) / N - Math.PI / 2;
            pts.push(`${{cx + radius * level * Math.cos(angle)}},${{cy + radius * level * Math.sin(angle)}}`);
        }}
        svg.innerHTML += `<polygon points="${{pts.join(' ')}}" fill="none" stroke="#334155" stroke-width="1"/>`;
    }});

    let compPts = [], secPts = [];
    metrics.forEach((m, i) => {{
        const angle = (Math.PI * 2 * i) / N - Math.PI / 2;
        const xEnd = cx + radius * Math.cos(angle);
        const yEnd = cy + radius * Math.sin(angle);
        svg.innerHTML += `<line x1="${{cx}}" y1="${{cy}}" x2="${{xEnd}}" y2="${{yEnd}}" stroke="#334155" stroke-width="1"/>`;

        const lx = cx + (radius + 24) * Math.cos(angle);
        const ly = cy + (radius + 16) * Math.sin(angle);
        svg.innerHTML += `<text x="${{lx}}" y="${{ly}}" fill="#94a3b8" font-size="10" text-anchor="middle" dominant-baseline="middle">${{m.label}}</text>`;

        const found = comparisons.find(c => c.metric === m.key) || {{ company_value: 0, sector_mean: 1 }};
        const cVal = found.company_value || 0;
        const sVal = found.sector_mean || 0.1;

        // Sektör ortalamasını 0.60 referans yarıçapına sabitleyip şirketi orantıla
        let ratio = sVal !== 0 ? (cVal / Math.abs(sVal)) * 0.60 : 0.5;
        if (cVal < 0) ratio = 0.12;
        const normComp = Math.min(1.0, Math.max(0.1, ratio));
        const normSec = 0.60;

        compPts.push(`${{cx + radius * normComp * Math.cos(angle)}},${{cy + radius * normComp * Math.sin(angle)}}`);
        secPts.push(`${{cx + radius * normSec * Math.cos(angle)}},${{cy + radius * normSec * Math.sin(angle)}}`);
    }});

    svg.innerHTML += `<polygon points="${{secPts.join(' ')}}" fill="rgba(245, 158, 11, 0.18)" stroke="#f59e0b" stroke-width="2"/>`;
    svg.innerHTML += `<polygon points="${{compPts.join(' ')}}" fill="rgba(56, 189, 248, 0.28)" stroke="#38bdf8" stroke-width="2.5"/>`;
}}

function drawBarChart(comparisons) {{
    const svg = document.getElementById('barSvg');
    svg.innerHTML = '';
    const keys = ['current_ratio', 'financial_leverage', 'net_profit_margin', 'roa', 'roe', 'asset_turnover'];
    const labels = ['Cari Oran', 'Kaldıraç', 'Net Kâr M.', 'ROA', 'ROE', 'Aktif Devir'];

    const chartH = 180, baseY = 195, startX = 45, groupW = 102;
    svg.innerHTML += `<line x1="30" y1="${{baseY}}" x2="660" y2="${{baseY}}" stroke="#475569" stroke-width="1.5"/>`;

    keys.forEach((k, idx) => {{
        const item = comparisons.find(c => c.metric === k) || {{ company_value: 0, sector_mean: 0 }};
        const cVal = item.company_value || 0;
        const sVal = item.sector_mean || 0;
        const maxLocal = Math.max(Math.abs(cVal), Math.abs(sVal), 0.5);

        const cH = Math.min(150, (Math.abs(cVal) / maxLocal) * 120);
        const sH = Math.min(150, (Math.abs(sVal) / maxLocal) * 120);

        const x = startX + idx * groupW;
        const cColor = cVal < 0 ? '#ef4444' : '#38bdf8';

        svg.innerHTML += `<rect x="${{x}}" y="${{baseY - cH}}" width="26" height="${{cH}}" fill="${{cColor}}" rx="4"/>`;
        svg.innerHTML += `<rect x="${{x + 30}}" y="${{baseY - sH}}" width="26" height="${{sH}}" fill="#f59e0b" rx="4"/>`;

        svg.innerHTML += `<text x="${{x + 13}}" y="${{baseY - cH - 6}}" fill="#e2e8f0" font-size="10" text-anchor="middle">${{cVal.toFixed(2)}}</text>`;
        svg.innerHTML += `<text x="${{x + 43}}" y="${{baseY - sH - 6}}" fill="#94a3b8" font-size="10" text-anchor="middle">${{sVal.toFixed(2)}}</text>`;
        svg.innerHTML += `<text x="${{x + 28}}" y="${{baseY + 18}}" fill="#cbd5e1" font-size="11" text-anchor="middle">${{labels[idx]}}</text>`;
    }});
}}

function renderAllCompaniesTable() {{
    const tbody = document.getElementById('allCompaniesTableBody');
    tbody.innerHTML = '';

    DATA.companies.forEach(c => {{
        const rep = DATA.hybrid_reports[c.code];
        const comp = DATA.comparisons[c.code].comparisons;
        const getVal = (m) => {{
            const f = comp.find(x => x.metric === m);
            return f && f.company_value !== null ? f.company_value : 0;
        }};

        const tagCls = rep.hybrid_risk_score >= 55 ? 'tag-high' : (rep.hybrid_risk_score >= 25 ? 'tag-med' : 'tag-low');

        tbody.innerHTML += `
            <tr style="cursor: pointer;" onclick="document.getElementById('companySelect').value='${{c.code}}'; renderSelectedCompany();">
                <td><strong>${{c.code}}</strong></td>
                <td>${{c.name}}</td>
                <td>${{c.sector}}</td>
                <td>${{getVal('current_ratio').toFixed(2)}}</td>
                <td>${{getVal('financial_leverage').toFixed(2)}}</td>
                <td>%${{(getVal('net_profit_margin') * 100).toFixed(1)}}</td>
                <td>%${{(getVal('roe') * 100).toFixed(1)}}</td>
                <td>${{rep.statistical_rule_score.toFixed(1)}}</td>
                <td>${{rep.isolation_forest_score.toFixed(1)}}</td>
                <td><strong>${{rep.hybrid_risk_score.toFixed(1)}} / 100</strong></td>
                <td><span class="tag ${{tagCls}}">${{rep.hybrid_risk_level}}</span></td>
            </tr>
        `;
    }});
}}

function runLiveSimulation() {{
    const name = document.getElementById('simName').value || 'Simülasyon A.Ş.';
    const sector = document.getElementById('simSector').value;
    const curAssets = parseFloat(document.getElementById('simCurAssets').value) || 0;
    const inv = parseFloat(document.getElementById('simInventories').value) || 0;
    const cash = parseFloat(document.getElementById('simCash').value) || 0;
    const totalAssets = parseFloat(document.getElementById('simTotalAssets').value) || 1;
    const shortDebt = parseFloat(document.getElementById('simShortDebt').value) || 1;
    const totalDebt = parseFloat(document.getElementById('simTotalDebt').value) || 0;
    const equity = parseFloat(document.getElementById('simEquity').value) || 1;
    const sales = parseFloat(document.getElementById('simSales').value) || 1;
    const netProfit = parseFloat(document.getElementById('simNetProfit').value) || 0;

    const curRatio = curAssets / shortDebt;
    const acidRatio = (curAssets - inv) / shortDebt;
    const lev = totalDebt / totalAssets;
    const npm = netProfit / sales;
    const roa = netProfit / totalAssets;

    let penalty = 0;
    let flags = [];
    if (curRatio < 1.0) {{ penalty += 20; flags.push('Cari Oran < 1.0'); }}
    if (acidRatio < 0.6) {{ penalty += 10; flags.push('Asit-Test < 0.6'); }}
    if (lev > 0.80) {{ penalty += 20; flags.push('Yüksek Borçluluk (>%80)'); }}
    if (equity < 0) {{ penalty += 25; flags.push('Negatif Özkaynak'); }}
    if (npm < -0.05) {{ penalty += 15; flags.push('Net Zarar'); }}

    const bench = DATA.sector_benchmarks[sector] || {{}};
    const secCur = (bench['liquidity.current_ratio'] || {{}}).mean || 1.5;
    const secLev = (bench['leverage.financial_leverage'] || {{}}).mean || 0.5;

    const box = document.getElementById('simResultBox');
    const flagText = flags.length > 0 ? `Uyarılar: ${{flags.join(', ')}}` : 'Finansal göstergeler dengeli.';
    box.innerHTML = `[${{name}}] Cari Oran: ${{curRatio.toFixed(2)}} (Sektör: ${{secCur.toFixed(2)}}) | Kaldıraç: ${{lev.toFixed(2)}} (Sektör: ${{secLev.toFixed(2)}}) | Net Kâr Marjı: %${{(npm*100).toFixed(1)}} | Tahmini Risk Puanı: ${{Math.min(100, penalty)}}/100 (${{flagText}})`;
}}

window.addEventListener('DOMContentLoaded', initDashboard);
</script>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return os.path.abspath(output_path)

    @staticmethod
    def serve_dashboard(port: int = 8080):
        """Yerel HTTP sunucusu başlatarak dashboard.html dosyasını sunar."""
        server = HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler)
        print(f"Web Dashboard sunucusu başlatıldı: http://127.0.0.1:{port}/dashboard.html")
        server.serve_forever()
