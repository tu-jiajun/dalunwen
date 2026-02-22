from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import os
from plots import (
    generate_trend_plot, 
    generate_treatment_plot, 
    generate_map_plot, 
    generate_weights_plot, 
    generate_failure_plot,
    generate_survival_plots
)

router = APIRouter(
    prefix="/api/analysis",
    tags=["analysis"]
)

# ==========================================
# Helper
# ==========================================
def make_html_response(chart_html: str) -> str:
    """
    Wrap the chart HTML snippet in a full HTML document with ECharts library.
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Chart</title>
        <script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js"></script>
        <style>
            body {{ margin: 0; padding: 0; }}
            .chart-container {{ width: 100%; height: 100vh; }}
        </style>
    </head>
    <body>
        {chart_html}
    </body>
    </html>
    """

# ==========================================
# Data Loading
# ==========================================
DATA_PATH = os.path.join(os.path.dirname(__file__), "../mock/11月19日需要确认excel_飞书.xlsx")

def get_data(sheet_name: str = '免疫联合治疗'):
    """
    Load data from the mock Excel file.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found at {DATA_PATH}")
    
    try:
        df = pd.read_excel(DATA_PATH, sheet_name=sheet_name)
        return df
    except Exception as e:
        raise Exception(f"Failed to load data from {DATA_PATH}: {str(e)}")

# ==========================================
# Analysis Endpoints
# ==========================================

@router.get("/trend")
async def analyze_trend():
    """
    [MOCK] 历年注册试验数量趋势分析图表 (Bar + Line)
    """
    try:
        df = get_data(sheet_name='免疫联合治疗')
        chart_html = generate_trend_plot(df)
        return HTMLResponse(content=make_html_response(chart_html))
    except Exception as e:
        return JSONResponse(status_code=500, content={"code": 500, "msg": f"Analysis failed: {str(e)}"})

@router.get("/treatment")
async def analyze_treatment():
    """
    [MOCK] 不同治疗方式的年度注册数量 (Stacked Bar + Line)
    """
    try:
        df = get_data(sheet_name='免疫联合治疗')
        chart_html = generate_treatment_plot(df)
        return HTMLResponse(content=make_html_response(chart_html))
    except Exception as e:
        return JSONResponse(status_code=500, content={"code": 500, "msg": f"Analysis failed: {str(e)}"})

@router.get("/map")
async def analyze_map():
    """
    [MOCK] Clinical Trials Count by Country (World Map)
    """
    try:
        df = get_data(sheet_name='免疫联合治疗')
        chart_html = generate_map_plot(df)
        return HTMLResponse(content=make_html_response(chart_html))
    except Exception as e:
        return JSONResponse(status_code=500, content={"code": 500, "msg": f"Analysis failed: {str(e)}"})

@router.get("/weights")
async def analyze_weights():
    """
    [MOCK] Weights of Main Categories (Cox Model -> Pie Chart)
    """
    try:
        df = get_data(sheet_name='免疫联合治疗')
        chart_html = generate_weights_plot(df)
        return HTMLResponse(content=make_html_response(chart_html))
    except Exception as e:
        return JSONResponse(status_code=500, content={"code": 500, "msg": f"Analysis failed: {str(e)}"})

@router.get("/failure")
async def analyze_failure():
    """
    [MOCK] Failure Reasons Distribution (Pie Chart)
    """
    try:
        # Note: Failure data is in a different sheet
        df = get_data(sheet_name='含有失败原因')
        chart_html = generate_failure_plot(df)
        return HTMLResponse(content=make_html_response(chart_html))
    except Exception as e:
        return JSONResponse(status_code=500, content={"code": 500, "msg": f"Analysis failed: {str(e)}"})

@router.get("/survival")
async def analyze_survival():
    """
    [MOCK] Survival Curves for categorical variables (Tabs with Line Charts)
    """
    try:
        df = get_data(sheet_name='免疫联合治疗')
        chart_html = generate_survival_plots(df)
        return HTMLResponse(content=make_html_response(chart_html))
    except Exception as e:
        return JSONResponse(status_code=500, content={"code": 500, "msg": f"Analysis failed: {str(e)}"})
