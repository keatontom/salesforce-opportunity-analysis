import tempfile
import os
from fastapi import UploadFile, HTTPException
from .analysis import analyze_opportunities
from .visualization import generate_visualizations
import traceback

async def comprehensive_report_analysis(file: UploadFile, date_range: str = 'all'):
    if not file or not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        try:
            # Get all analysis results with date filtering
            analysis_results = analyze_opportunities(tmp_file_path, date_range)
            visualizations = generate_visualizations(tmp_file_path, date_range)
            
            return {
                "Advanced Analysis": analysis_results,
                "Visualizations": visualizations
            }
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        finally:
            os.unlink(tmp_file_path)
    except Exception as e:
        print(f"File handling error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")