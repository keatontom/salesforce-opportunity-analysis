import tempfile
import os
import logging
from fastapi import UploadFile, HTTPException
from analysis import analyze_opportunities
from visualization import generate_visualizations
import traceback
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def comprehensive_report_analysis(file: UploadFile, date_range: str = 'all'):
    """
    Process and analyze a sales opportunity CSV file.
    
    Args:
        file: The uploaded CSV file
        date_range: The date range to filter the data ('all', 'ytd', 'q1', 'q2', 'q3', 'q4')
        
    Returns:
        Dict containing analysis results and visualizations
        
    Raises:
        HTTPException: For various file processing and analysis errors
    """
    if not file or not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        try:
            # Validate CSV file
            try:
                df = pd.read_csv(tmp_file_path)
                if df.empty:
                    raise HTTPException(status_code=400, detail="The CSV file is empty")
                    
                required_columns = [
                    'Account Name', 'Opportunity Name', 'Stage', 'Close Date', 
                    'Created Date', 'Type', 'Total ACV', 'Primary Campaign Source',
                    'Closed Lost Reason', 'Law Firm Practice Area', 'NumofLawyers'
                ]
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Missing required columns: {', '.join(missing_columns)}"
                    )
            except pd.errors.EmptyDataError:
                raise HTTPException(status_code=400, detail="The CSV file is empty")
            except pd.errors.ParserError:
                raise HTTPException(status_code=400, detail="Invalid CSV file format")

            # Perform analysis
            analysis_results = analyze_opportunities(tmp_file_path, date_range)
            visualizations = generate_visualizations(tmp_file_path, date_range)
            
            return {
                "Advanced Analysis": analysis_results,
                "Visualizations": visualizations
            }
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except Exception as e:
                logger.error(f"Error deleting temporary file: {str(e)}")
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")