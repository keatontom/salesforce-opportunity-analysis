import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Union, TypeVar
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T', bound=Union[Dict[str, Any], List[Any], int, float, str, None])

def convert_numpy_types(obj: T) -> T:
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)  # type: ignore
    elif isinstance(obj, np.floating):
        return float(obj)  # type: ignore
    elif isinstance(obj, np.ndarray):
        return obj.tolist()  # type: ignore
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}  # type: ignore
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]  # type: ignore
    return obj

class SalesOpportunityAnalyzer:
    def __init__(self, data: pd.DataFrame, date_range: str = 'all'):
        """
        Initialize the analyzer with sales opportunity data
        
        Actual columns:
        - Account Name
        - Opportunity Name
        - Stage
        - Close Date
        - Created Date
        - Type (replaces Product/Service)
        - Total ACV
        - Primary Campaign Source
        - Closed Lost Reason
        - Law Firm Practice Area
        - NumofLawyers
        """
        logger.info(f"Initializing analyzer with data shape: {data.shape}")
        logger.info(f"Columns in data: {data.columns.tolist()}")
        logger.info(f"Sample of data:\n{data.head()}")
        
        self.data = data
        self.validate_columns()
        self.prepare_data()
        self.filter_by_date_range(date_range)
        
        logger.info(f"After initialization and filtering, data shape: {self.data.shape}")
        logger.info(f"Unique stages: {self.data['Stage'].unique()}")
        logger.info(f"Stage distribution:\n{self.data['Stage'].value_counts()}")
    
    def validate_columns(self):
        """
        Check required columns and provide defaults if missing
        """
        required_columns = {
            'Account Name': 'object',
            'Opportunity Name': 'object',
            'Stage': 'object',
            'Close Date': 'datetime64',
            'Created Date': 'datetime64',
            'Type': 'object',
            'Total ACV': 'float64',
            'Primary Campaign Source': 'object',
            'Closed Lost Reason': 'object',
            'Law Firm Practice Area': 'object',
            'NumofLawyers': 'float64'
        }
        
        logger.info("Validating columns...")
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            logger.warning(f"Missing columns: {missing_columns}")
        
        # Add missing columns with default values
        for col, dtype in required_columns.items():
            if col not in self.data.columns:
                if dtype == 'object':
                    self.data[col] = 'Unknown'
                elif dtype.startswith('float'):
                    self.data[col] = 0.0
                elif dtype.startswith('datetime'):
                    self.data[col] = pd.Timestamp.now()
                logger.warning(f"Added missing column '{col}' with default values")
        
        # Convert numeric columns
        try:
            self.data['Total ACV'] = pd.to_numeric(self.data['Total ACV'], errors='coerce').fillna(0)
            self.data['NumofLawyers'] = pd.to_numeric(self.data['NumofLawyers'], errors='coerce').fillna(0)
            logger.info("Numeric columns converted successfully")
        except Exception as e:
            logger.error(f"Error converting numeric columns: {str(e)}")

    def prepare_data(self):
        """
        Preprocess and transform the raw data
        """
        logger.info("Starting data preparation")
        # Convert date columns, handling potential format issues
        for date_col in ['Created Date', 'Close Date']:
            try:
                self.data[date_col] = pd.to_datetime(self.data[date_col], errors='coerce')
                logger.info(f"Converted {date_col} to datetime")
            except Exception as e:
                logger.error(f"Error converting {date_col}: {str(e)}")
                logger.warning(f"Using current date for {date_col}")
                self.data[date_col] = pd.Timestamp.now()
        
        # Calculate time to close
        self.data['Time_To_Close'] = (self.data['Close Date'] - self.data['Created Date']).dt.days
        logger.info("Calculated Time_To_Close")
        logger.info(f"Data shape after preparation: {self.data.shape}")

    def filter_by_date_range(self, date_range: str):
        """
        Filter data based on date range (currently disabled - showing all data)
        """
        logger.info("Date filtering disabled - showing all data")
        return
    
    def calculate_core_metrics(self) -> Dict[str, Any]:
        """
        Calculate core sales metrics
        """
        total_opportunities = len(self.data)
        won_opportunities = len(self.data[self.data['Stage'] == 'Won'])
        
        # Prevent division by zero
        win_rate = (won_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0
        avg_deal_size = self.data['Total ACV'].mean() if not self.data['Total ACV'].empty else 0
        avg_time_to_close = self.data['Time_To_Close'].mean() if not self.data['Time_To_Close'].empty else 0
        
        metrics = {
            "Total Volume": round(self.data['Total ACV'].sum(), 2),
            "Average Deal Size": round(avg_deal_size, 2),
            "Win Rate": round(win_rate, 2),
            "Average Time to Close": round(avg_time_to_close, 2),
            "Number of Opportunities": total_opportunities
        }
        
        return convert_numpy_types(metrics)
    
    def calculate_trends(self) -> Dict[str, Any]:
        """
        Calculate monthly trends for key metrics
        """
        monthly_data = self.data.set_index('Created Date').resample('M').agg({
            'Total ACV': ['sum', 'mean'],
            'Opportunity Name': 'count',
            'Stage': lambda x: (x == 'Won').mean()
        })
        
        monthly_data.columns = ['Total Volume', 'Average Deal Size', 'Number of Deals', 'Win Rate']
        monthly_data.index = pd.to_datetime(monthly_data.index).strftime('%Y-%m')
        
        return {
            "labels": monthly_data.index.tolist(),
            "metrics": {
                "Total Volume": monthly_data['Total Volume'].tolist(),
                "Average Deal Size": monthly_data['Average Deal Size'].tolist(),
                "Number of Deals": monthly_data['Number of Deals'].tolist(),
                "Win Rate": monthly_data['Win Rate'].tolist()
            }
        }
    
    def segment_performance(self) -> Dict[str, Any]:
        """
        Analyze performance by different segments
        """
        # Performance by Account
        account_performance = self.data.groupby('Account Name').agg({
            'Total ACV': ['sum', 'mean'],
            'Stage': lambda x: (len(x[x == 'Won']) / len(x) * 100) if len(x) > 0 else 0  # Safe division
        }).reset_index()
        account_performance.columns = ['Account Name', 'Total Volume', 'Avg Deal Size', 'Win Rate']
        account_performance['Total Volume'] = account_performance['Total Volume'].round(2)
        account_performance['Avg Deal Size'] = account_performance['Avg Deal Size'].round(2)
        account_performance['Win Rate'] = account_performance['Win Rate'].round(2)
        
        # Performance by Type with opportunities
        type_performance = []
        for type_name in self.data['Type'].unique():
            type_data = self.data[self.data['Type'] == type_name]
            type_count = len(type_data)
            type_perf = {
                'Type': type_name,
                'Total Volume': round(type_data['Total ACV'].sum(), 2),
                'Avg Deal Size': round(type_data['Total ACV'].mean() if not type_data['Total ACV'].empty else 0, 2),
                'Win Rate': round((len(type_data[type_data['Stage'] == 'Won']) / type_count * 100) if type_count > 0 else 0, 2),
                'opportunities': type_data[[
                    'Account Name', 'Opportunity Name', 'Total ACV', 'Created Date', 'Type'
                ]].to_dict(orient='records')
            }
            type_performance.append(type_perf)
        
        # Performance by Practice Area
        valid_areas = self.data['Law Firm Practice Area'].notna()
        practice_areas_exploded = pd.DataFrame({
            'Practice Area': self.data[valid_areas]['Law Firm Practice Area'].str.split(';').explode().str.strip(),
            'Total ACV': self.data[valid_areas]['Total ACV'].repeat(
                (self.data[valid_areas]['Law Firm Practice Area'].str.count(';') + 1).tolist()
            ),
            'Stage': self.data[valid_areas]['Stage'].repeat(
                (self.data[valid_areas]['Law Firm Practice Area'].str.count(';') + 1).tolist()
            )
        })
        
        # Remove empty or 'Unknown' values
        practice_areas_exploded = practice_areas_exploded[
            practice_areas_exploded['Practice Area'].notna() & 
            (practice_areas_exploded['Practice Area'] != '') &
            (practice_areas_exploded['Practice Area'] != 'Unknown')
        ]
        
        # Group by individual practice areas with safe division
        practice_performance = practice_areas_exploded.groupby('Practice Area').agg({
            'Total ACV': ['sum', 'mean'],
            'Stage': lambda x: (len(x[x == 'Won']) / len(x) * 100) if len(x) > 0 else 0  # Safe division
        }).reset_index()
        practice_performance.columns = ['Practice Area', 'Total Volume', 'Avg Deal Size', 'Win Rate']
        practice_performance['Total Volume'] = practice_performance['Total Volume'].round(2)
        practice_performance['Avg Deal Size'] = practice_performance['Avg Deal Size'].round(2)
        practice_performance['Win Rate'] = practice_performance['Win Rate'].round(2)
        practice_performance = practice_performance.sort_values('Total Volume', ascending=False)
        
        return {
            "Account Performance": account_performance.to_dict(orient='records'),
            "Type Performance": type_performance,
            "Practice Area Performance": practice_performance.to_dict(orient='records')
        }
    
    def pipeline_health_analysis(self) -> Dict[str, Any]:
        """
        Analyze the health of the sales pipeline
        """
        total_opportunities = len(self.data)
        stage_distribution = {}
        for stage in self.data['Stage'].unique():
            stage_data = self.data[self.data['Stage'] == stage]
            count = len(stage_data)
            
            stage_distribution[stage] = {
                'percentage': float(count / total_opportunities) if total_opportunities > 0 else 0,
                'count': int(count)
            }
        
        # Lost opportunity analysis
        lost_reasons = self.data[self.data['Stage'] == 'Lost']['Closed Lost Reason'].value_counts()
        
        # Aging opportunities
        aging_opportunities = self.data.copy()
        current_time = pd.Timestamp.now(tz='UTC')
        aging_opportunities['Created Date'] = pd.to_datetime(aging_opportunities['Created Date']).dt.tz_localize('UTC')
        aging_opportunities['Days Open'] = aging_opportunities['Created Date'].apply(lambda x: (current_time - x).days)
        
        aging_opportunities = aging_opportunities[
            (aging_opportunities['Stage'] != 'Won') & 
            (aging_opportunities['Stage'] != 'Lost') & 
            (aging_opportunities['Days Open'] > 90)
        ]
        
        aging_details = aging_opportunities[[
            'Account Name', 'Opportunity Name', 'Total ACV', 'Created Date', 'Stage', 'Days Open'
        ]].copy()
        aging_details['Created Date'] = aging_details['Created Date'].dt.strftime('%Y-%m-%d')
        
        return {
            "Stage Distribution": stage_distribution,
            "Lost Reasons": lost_reasons.to_dict(),
            "Aging Opportunities": {
                "Count": len(aging_opportunities),
                "Total Value": aging_opportunities['Total ACV'].sum(),
                "Details": aging_details.to_dict(orient='records')
            }
        }
    
    def analyze_practice_area_stats(self, opportunities: pd.DataFrame) -> List[Dict[str, Any]]:
        """Helper method to consistently analyze practice areas for both won and lost opportunities"""
        practice_stats = []
        all_practices = set()
        current_stage = opportunities['Stage'].iloc[0]  # 'Won' or 'Lost'
        total_stage_opps = len(opportunities)  # Total won or lost opportunities
        
        # First, collect all unique practice areas
        for practices in self.data['Law Firm Practice Area'].dropna():
            if isinstance(practices, str):
                # Filter out 'other' and similar categories
                practices_filtered = [
                    p.strip() for p in practices.split(';') 
                    if p.strip() and p.strip().lower() not in ['unknown', 'other', 'others', 'n/a']
                ]
                all_practices.update(practices_filtered)
        
        # Create a DataFrame to store practice area metrics
        practice_metrics = []
        
        for practice in all_practices:
            # For each practice area, look at opportunities that include this practice
            practice_mask = opportunities['Law Firm Practice Area'].fillna('').str.contains(practice, regex=False, case=False, na=False)
            practice_opps = opportunities[practice_mask]
            
            if len(practice_opps) > 0:
                # Calculate the percentage this practice area represents of all won/lost opportunities
                practice_percentage = (len(practice_opps) / total_stage_opps) * 100
                practice_value = practice_opps['Total ACV'].sum()
                
                practice_metrics.append({
                    'practice': practice,
                    'count': len(practice_opps),
                    'total_count': total_stage_opps,
                    'value': practice_value,
                    'percentage': practice_percentage,
                    'value_per_opp': practice_value / len(practice_opps)
                })
        
        # Convert to DataFrame for easier sorting
        if practice_metrics:
            df = pd.DataFrame(practice_metrics)
            
            # Sort by percentage and value
            df = df.sort_values(['percentage', 'value'], ascending=[False, False])
            
            # Convert to required format
            for _, row in df.iterrows():
                practice_stats.append({
                    'practice': row['practice'],
                    'text': f"  • {row['practice']}: {row['percentage']:.1f}% {current_stage.lower()} ({int(row['count'])}/{int(row['total_count'])} {current_stage.lower()}, ${row['value']:,.2f})",
                    'rate': row['percentage'],
                    'value': row['value'],
                    'count': row['count']
                })
        
        return practice_stats
    
    def analyze_loss_patterns(self) -> Dict[str, Any]:
        """
        Analyze patterns in lost opportunities
        """
        lost_opps = self.data[self.data['Stage'] == 'Lost'].copy()
        
        if len(lost_opps) == 0:
            return {"message": "No lost opportunities to analyze", "has_data": False}
        
        # Analyze Lost Reasons
        lost_reasons = lost_opps['Closed Lost Reason'].value_counts()
        total_lost = len(lost_opps)
        
        reason_stats = []
        for reason, count in lost_reasons.items():
            value = lost_opps[lost_opps['Closed Lost Reason'] == reason]['Total ACV'].sum()
            loss_rate = (count/total_lost*100) if total_lost > 0 else 0
            reason_stats.append({
                'reason': reason,
                'text': f"• {reason} ({loss_rate:.1f}%): {count} losses (${value:,.2f} total value)",
                'count': count,
                'value': value
            })
        
        # Sort by count and value
        reason_stats.sort(key=lambda x: (-x['count'], -x['value']))
        reason_summary = [item['text'] for item in reason_stats[:5]]  # Top 5 reasons

        # Analyze by Type
        type_stats = []
        for type_name in self.data['Type'].unique():
            type_data = self.data[self.data['Type'] == type_name]
            total_type = len(type_data)
            lost_type = len(type_data[type_data['Stage'] == 'Lost'])
            if total_type >= 5:  # Only include types with meaningful sample size
                loss_rate = (lost_type / total_type * 100) if total_type > 0 else 0
                lost_value = type_data[type_data['Stage'] == 'Lost']['Total ACV'].sum()
                type_stats.append({
                    'type': type_name,
                    'text': f"  • {type_name}: {loss_rate:.1f}% loss rate ({lost_type}/{total_type} lost, ${lost_value:,.2f})",
                    'loss_rate': loss_rate,
                    'value': lost_value
                })

        # Sort by loss rate and value
        type_stats.sort(key=lambda x: (-x['loss_rate'], -x['value']))
        type_summary = [item['text'] for item in type_stats]

        # Analyze by Firm Size
        size_bins = [0, 50, 200, 500, float('inf')]
        size_labels = ['Small (0-50)', 'Medium (51-200)', 'Large (201-500)', 'Enterprise (500+)']
        lost_opps['Size Category'] = pd.cut(lost_opps['NumofLawyers'], bins=size_bins, labels=size_labels)
        size_loss_rate = lost_opps.groupby('Size Category', observed=True).agg({
            'Opportunity Name': 'count',
            'Total ACV': 'sum'
        })

        size_summary = []
        for size in size_loss_rate.index:
            count = size_loss_rate.loc[size, 'Opportunity Name']
            value = size_loss_rate.loc[size, 'Total ACV']
            size_summary.append(f"  • {size.replace('Small', '0-50 Lawyers').replace('Medium', '51-200 Lawyers').replace('Large', '201-500 Lawyers').replace('Enterprise', '500+ Lawyers').replace(' (', ' (').replace(')', '')}: {count} losses (${value:,.2f} total value)")

        # Analyze Practice Areas
        practice_stats = self.analyze_practice_area_stats(lost_opps)
        practice_stats.sort(key=lambda x: (-x['rate'], -x['value']))
        practice_summary = [item['text'] for item in practice_stats[:5]]  # Top 5

        # Analyze Campaigns
        def categorize_campaign(campaign):
            if pd.isna(campaign) or str(campaign).lower().strip() in ['', 'unknown', 'other', 'none']:
                return None
            campaign = str(campaign).lower()
            if 'email' in campaign or 'newsletter' in campaign:
                return 'Email Campaigns'
            elif 'demo' in campaign:
                return 'Product Demos'
            elif 'webinar' in campaign or 'event' in campaign:
                return 'Events & Webinars'
            elif 'referral' in campaign:
                return 'Referrals'
            elif 'partner' in campaign:
                return 'Partner Programs'
            elif 'social' in campaign:
                return 'Social Media'
            elif 'content' in campaign or 'blog' in campaign:
                return 'Content Marketing'
            else:
                return campaign.title()

        lost_opps['Campaign Category'] = lost_opps['Primary Campaign Source'].apply(categorize_campaign)
        lost_opps_with_campaigns = lost_opps[lost_opps['Campaign Category'].notna()]
        campaign_stats = lost_opps_with_campaigns.groupby('Campaign Category', observed=False).agg({
            'Opportunity Name': 'count',
            'Total ACV': 'sum'
        })

        campaign_summary = []
        for campaign in campaign_stats.index:
            count = int(pd.to_numeric(campaign_stats.loc[campaign, 'Opportunity Name']))
            value = campaign_stats.loc[campaign, 'Total ACV']
            if count >= 2:  # Lower threshold to show more campaigns
                campaign_summary.append({
                    'campaign': campaign,
                    'text': f"  • {campaign}: {count} losses (${value:,.2f} total value)",
                    'count': count,
                    'value': value
                })

        # Sort by count and value and take top 3
        campaign_summary.sort(key=lambda x: (-x['count'], -x['value']))
        campaign_text = [item['text'] for item in campaign_summary[:3]]  # Take top 3

        return {
            "has_data": True,
            "total_lost": total_lost,
            "total_value_lost": lost_opps['Total ACV'].sum(),
            "avg_value_lost": lost_opps['Total ACV'].mean() if not lost_opps['Total ACV'].empty else 0,
            "avg_cycle_length": int(round(lost_opps['Time_To_Close'].mean())) if not lost_opps['Time_To_Close'].empty else 0,
            "insights": [
                {
                    "category": "Practice Area Failures",
                    "finding": "\n".join(practice_summary) if 'practice_summary' in locals() else "No practice area data available",
                    "severity": "high"
                },
                {
                    "category": "Type Performance",
                    "finding": "\n".join(type_summary),
                    "severity": "high" if any(x['loss_rate'] > 75 for x in type_stats) else "medium"
                },
                {
                    "category": "Campaign Performance",
                    "finding": "\n".join(campaign_text) if 'campaign_text' in locals() and campaign_text else "No significant campaign data available",
                    "severity": "medium"
                },
                {
                    "category": "Failure Reasons",
                    "finding": "\n".join(reason_summary),
                    "severity": "high"
                },
                {
                    "category": "Lawyer Count Distribution",
                    "finding": "\n".join(size_summary) if 'size_summary' in locals() else "No lawyer count data available",
                    "severity": "medium"
                }
            ]
        }
    
    @staticmethod
    def categorize_campaign(campaign: str) -> str | None:
        """Categorize campaign sources into standardized categories"""
        if pd.isna(campaign) or str(campaign).lower().strip() in ['', 'unknown', 'other', 'none']:
            return None
        campaign = str(campaign).lower()
        if 'email' in campaign or 'newsletter' in campaign:
            return 'Email Campaigns'
        elif 'demo' in campaign:
            return 'Product Demos'
        elif 'webinar' in campaign or 'event' in campaign:
            return 'Events & Webinars'
        elif 'referral' in campaign:
            return 'Referrals'
        elif 'partner' in campaign:
            return 'Partner Programs'
        elif 'social' in campaign:
            return 'Social Media'
        elif 'content' in campaign or 'blog' in campaign:
            return 'Content Marketing'
        else:
            return campaign.title()

    def analyze_win_patterns(self) -> Dict[str, Any]:
        """
        Analyze patterns in won opportunities
        """
        won_opps = self.data[self.data['Stage'] == 'Won'].copy()
        
        if len(won_opps) == 0:
            return {"message": "No won opportunities to analyze", "has_data": False}

        # Calculate core metrics
        total_won = len(won_opps)
        total_value_won = won_opps['Total ACV'].sum()
        avg_cycle_length = int(round(won_opps['Time_To_Close'].mean())) if not won_opps['Time_To_Close'].empty else 0

        # Analyze by Firm Size
        size_bins = [0, 50, 200, 500, float('inf')]
        size_labels = ['Small (0-50)', 'Medium (51-200)', 'Large (201-500)', 'Enterprise (500+)']
        won_opps['Size Category'] = pd.cut(won_opps['NumofLawyers'], bins=size_bins, labels=size_labels)
        size_win_rate = won_opps.groupby('Size Category', observed=True).agg({
            'Opportunity Name': 'count',
            'Total ACV': 'sum'
        })

        size_summary = []
        for size in size_win_rate.index:
            count = size_win_rate.loc[size, 'Opportunity Name']
            value = size_win_rate.loc[size, 'Total ACV']
            size_summary.append(f"  • {size.replace('Small', '0-50 Lawyers').replace('Medium', '51-200 Lawyers').replace('Large', '201-500 Lawyers').replace('Enterprise', '500+ Lawyers').replace(' (', ' (').replace(')', '')}: {count} wins (${value:,.2f} total value)")

        # Analyze Practice Areas
        practice_stats = self.analyze_practice_area_stats(won_opps)
        practice_stats.sort(key=lambda x: (-x['rate'], -x['value']))
        practice_summary = [item['text'] for item in practice_stats[:5]]  # Top 5

        # Analyze by Type
        type_stats = []
        for type_name in self.data['Type'].unique():
            type_data = self.data[self.data['Type'] == type_name]
            total_type = len(type_data)
            won_type = len(type_data[type_data['Stage'] == 'Won'])
            if total_type >= 5:  # Only include types with meaningful sample size
                win_rate = (won_type / total_type * 100) if total_type > 0 else 0
                value = type_data[type_data['Stage'] == 'Won']['Total ACV'].sum()
                type_stats.append({
                    'type': type_name,
                    'text': f"  • {type_name}: {win_rate:.1f}% win rate ({won_type}/{total_type} won, ${value:,.2f})",
                    'win_rate': win_rate,
                    'value': value
                })

        # Sort by win rate and value
        type_stats.sort(key=lambda x: (-x['win_rate'], -x['value']))
        type_summary = [item['text'] for item in type_stats]

        # Analyze Campaigns
        won_opps['Campaign Category'] = won_opps['Primary Campaign Source'].apply(self.categorize_campaign)
        won_opps_with_campaigns = won_opps[won_opps['Campaign Category'].notna()]
        campaign_stats = won_opps_with_campaigns.groupby('Campaign Category', observed=True).agg({
            'Opportunity Name': 'count',
            'Total ACV': 'sum'
        })

        campaign_summary = []
        for campaign in campaign_stats.index:
            count = int(pd.to_numeric(campaign_stats.loc[campaign, 'Opportunity Name']))
            value = campaign_stats.loc[campaign, 'Total ACV']
            if count >= 2:  # Lower threshold to show more campaigns
                total_campaign = len(self.data[self.data['Primary Campaign Source'].str.contains(campaign, na=False, case=False)])
                if total_campaign > 0:  # Prevent division by zero
                    win_rate = count / total_campaign * 100
                    campaign_summary.append({
                        'campaign': campaign,
                        'text': f"  • {campaign}: {count} wins (${value:,.2f} total value)",
                        'win_rate': win_rate,
                        'value': value,
                        'count': count
                    })

        # Sort by count and value and take top 3
        campaign_summary.sort(key=lambda x: (-x['count'], -x['value']))
        campaign_text = [item['text'] for item in campaign_summary[:3]]

        return {
            "has_data": True,
            "total_won": total_won,
            "total_value_won": total_value_won,
            "avg_value_won": total_value_won / total_won if total_won > 0 else 0,
            "avg_cycle_length": avg_cycle_length,
            "insights": [
                {
                    "category": "Practice Area Successes",
                    "finding": "\n".join(practice_summary) if practice_summary else "No practice area data available",
                    "severity": "high"
                },
                {
                    "category": "Type Performance",
                    "finding": "\n".join(type_summary),
                    "severity": "medium"
                },
                {
                    "category": "Campaign Performance",
                    "finding": "\n".join(campaign_text) if campaign_text else "No significant campaign data available",
                    "severity": "medium"
                },
                {
                    "category": "Lawyer Count Distribution",
                    "finding": "\n".join(size_summary) if size_summary else "No lawyer count data available",
                    "severity": "medium"
                }
            ]
        }

    def score_open_opportunities(self) -> Dict[str, Any]:
        """
        Score open opportunities based on historical win/loss patterns
        Score represents the average of win rates across all matching fields
        """
        # Get open opportunities (not Won or Lost)
        open_opps = self.data[~self.data['Stage'].isin(['Won', 'Lost'])].copy()
        
        if len(open_opps) == 0:
            return {"message": "No open opportunities to analyze", "has_data": False}
            
        # Get historical data (closed opportunities)
        closed_opps = self.data[self.data['Stage'].isin(['Won', 'Lost'])].copy()
        
        if len(closed_opps) == 0:
            return {"message": "No historical data available for analysis", "has_data": False}
            
        # Calculate base win rate
        base_win_rate = (len(closed_opps[closed_opps['Stage'] == 'Won']) / len(closed_opps)) if len(closed_opps) > 0 else 0
        
        # Define size categories
        size_bins = [0, 50, 200, 500, float('inf')]
        size_labels = ['Small', 'Medium', 'Large', 'Enterprise']
        
        # Process each open opportunity
        scored_opportunities = []
        table_rows = []
        
        for _, opp in open_opps.iterrows():
            field_scores = []
            score_details = {}
            insights = []
            
            # 1. Practice Area
            if pd.notna(opp['Law Firm Practice Area']):
                practice_areas = [area.strip() for area in str(opp['Law Firm Practice Area']).split(';')]
                practice_win_rates = []
                
                for area in practice_areas:
                    area_opps = closed_opps[closed_opps['Law Firm Practice Area'].fillna('').str.contains(area, na=False)]
                    if len(area_opps) > 0:
                        area_win_rate = (len(area_opps[area_opps['Stage'] == 'Won']) / len(area_opps)) if len(area_opps) > 0 else 0
                        practice_win_rates.append(area_win_rate)
                
                if practice_win_rates:
                    practice_score = np.mean(practice_win_rates) * 100
                    field_scores.append(practice_score)
                    score_details['practice_area'] = [
                        f"{', '.join(practice_areas)}: {practice_score:.1f}% average win rate across practice areas"
                    ]
            
            # 2. Firm Size
            if pd.notna(opp['NumofLawyers']):
                opp_size = pd.cut([opp['NumofLawyers']], bins=size_bins, labels=size_labels)[0]
                if pd.notna(opp_size):
                    size_opps = closed_opps[pd.cut(closed_opps['NumofLawyers'], bins=size_bins, labels=size_labels) == opp_size]
                    if len(size_opps) > 0:
                        size_win_rate = (len(size_opps[size_opps['Stage'] == 'Won']) / len(size_opps) * 100) if len(size_opps) > 0 else 0
                        field_scores.append(size_win_rate)
                        score_details['firm_size'] = [
                            f"{opp_size} firms: {size_win_rate:.1f}% win rate"
                        ]
            
            # 3. Opportunity Type
            if pd.notna(opp['Type']):
                type_opps = closed_opps[closed_opps['Type'] == opp['Type']]
                if len(type_opps) > 0:
                    type_win_rate = (len(type_opps[type_opps['Stage'] == 'Won']) / len(type_opps) * 100) if len(type_opps) > 0 else 0
                    field_scores.append(type_win_rate)
                    score_details['opportunity_type'] = [
                        f"{opp['Type']}: {type_win_rate:.1f}% win rate"
                    ]
            
            # 4. Campaign Source
            if pd.notna(opp['Primary Campaign Source']):
                campaign_opps = closed_opps[closed_opps['Primary Campaign Source'] == opp['Primary Campaign Source']]
                if len(campaign_opps) > 0:
                    campaign_win_rate = (len(campaign_opps[campaign_opps['Stage'] == 'Won']) / len(campaign_opps) * 100) if len(campaign_opps) > 0 else 0
                    field_scores.append(campaign_win_rate)
                    score_details['campaign_source'] = [
                        f"{opp['Primary Campaign Source']}: {campaign_win_rate:.1f}% win rate"
                    ]
            
            # 5. Deal Size (similar value range)
            if pd.notna(opp['Total ACV']):
                value_range = (0.8 * opp['Total ACV'], 1.2 * opp['Total ACV'])
                value_opps = closed_opps[
                    (closed_opps['Total ACV'] >= value_range[0]) & 
                    (closed_opps['Total ACV'] <= value_range[1])
                ]
                if len(value_opps) > 0:
                    value_win_rate = (len(value_opps[value_opps['Stage'] == 'Won']) / len(value_opps) * 100) if len(value_opps) > 0 else 0
                    field_scores.append(value_win_rate)
                    avg_won_value = closed_opps[closed_opps['Stage'] == 'Won']['Total ACV'].mean() if not closed_opps[closed_opps['Stage'] == 'Won']['Total ACV'].empty else 0
                    value_ratio = (opp['Total ACV'] / avg_won_value) if avg_won_value > 0 else 1
                    score_details['deal_size'] = [
                        f"Similar deal sizes: {value_win_rate:.1f}% win rate (Deal value is {value_ratio*100:.1f}% of average)"
                    ]
            
            # Calculate final score as average of field scores
            if field_scores:
                final_score = round(np.mean(field_scores), 2)
            else:
                final_score = round(base_win_rate * 100, 2)
            
            # Determine risk level based on win probability
            risk_level = "Low" if final_score >= 70 else "Medium" if final_score >= 40 else "High"
            
            # Add insights for each field
            insights = []
            
            # Add all calculated percentages with sample sizes
            if 'practice_area' in score_details:
                total_wins = 0
                total_opps = 0
                practice_areas_list = []
                for area in practice_areas:
                    area_opps = closed_opps[closed_opps['Law Firm Practice Area'].fillna('').str.contains(area, na=False)]
                    if len(area_opps) > 0:
                        total_wins += len(area_opps[area_opps['Stage'] == 'Won'])
                        total_opps += len(area_opps)
                        practice_areas_list.append(area)
                
                if total_opps > 0:
                    combined_win_rate = (total_wins / total_opps) * 100 if total_opps > 0 else 0
                    insights.append(f"Practice Areas ({', '.join(practice_areas_list)}): {combined_win_rate:.1f}% win rate ({total_wins}/{total_opps} opportunities)")

            if 'firm_size' in score_details:
                size_opps = closed_opps[pd.cut(closed_opps['NumofLawyers'], bins=size_bins, labels=size_labels) == opp_size]
                if len(size_opps) > 0:
                    wins = len(size_opps[size_opps['Stage'] == 'Won'])
                    total = len(size_opps)
                    insights.append(f"Firm Size ({opp_size}): {size_win_rate:.1f}% win rate ({wins}/{total} opportunities)")

            if 'opportunity_type' in score_details:
                type_opps = closed_opps[closed_opps['Type'] == opp['Type']]
                if len(type_opps) > 0:
                    wins = len(type_opps[type_opps['Stage'] == 'Won'])
                    total = len(type_opps)
                    insights.append(f"Opportunity Type ({opp['Type']}): {type_win_rate:.1f}% win rate ({wins}/{total} opportunities)")

            if 'campaign_source' in score_details:
                campaign_opps = closed_opps[closed_opps['Primary Campaign Source'] == opp['Primary Campaign Source']]
                if len(campaign_opps) > 0:
                    wins = len(campaign_opps[campaign_opps['Stage'] == 'Won'])
                    total = len(campaign_opps)
                    insights.append(f"Campaign Source ({opp['Primary Campaign Source']}): {campaign_win_rate:.1f}% win rate ({wins}/{total} opportunities)")

            if 'deal_size' in score_details:
                value_opps = closed_opps[
                    (closed_opps['Total ACV'] >= value_range[0]) & 
                    (closed_opps['Total ACV'] <= value_range[1])
                ]
                if len(value_opps) > 0:
                    wins = len(value_opps[value_opps['Stage'] == 'Won'])
                    total = len(value_opps)
                    insights.append(f"Similar Deal Size (${value_range[0]:,.2f} - ${value_range[1]:,.2f}): {value_win_rate:.1f}% win rate ({wins}/{total} opportunities)")
            
            # Add final score insight
            fields_used = len(field_scores)
            insights.append(f"Final Score: {final_score:.1f}% based on average of {fields_used} criteria")
            
            # Create table row
            table_row = {
                "Opportunity": opp['Opportunity Name'],
                "Score": f"{final_score}%",
                "Risk": risk_level,
                "Value": f"${opp['Total ACV']:,.2f}",
                "Days Open": (datetime.now() - pd.to_datetime(opp['Created Date'])).days,
                "Score Details": {
                    factor: {
                        "score": "N/A",  # No individual scores in simplified version
                        "weight": "N/A",  # No weights in simplified version
                        "details": details
                    }
                    for factor, details in score_details.items()
                },
                "Key Insights": "\n".join(insights)  # Show all insights on separate lines
            }
            table_rows.append(table_row)
            
            # Add to scored opportunities
            scored_opportunities.append({
                "opportunity_name": opp['Opportunity Name'],
                "score": final_score,
                "risk_level": risk_level,
                "total_value": opp['Total ACV'],
                "days_open": (datetime.now() - pd.to_datetime(opp['Created Date'])).days,
                "score_details": score_details,
                "factor_scores": {"similar_opportunities": final_score},  # Simplified to single score
                "insights": insights
            })
        
        # Sort opportunities by score (descending)
        scored_opportunities.sort(key=lambda x: x['score'], reverse=True)
        table_rows.sort(key=lambda x: float(x['Score'].rstrip('%')), reverse=True)
        
        return {
            "has_data": True,
            "total_opportunities": len(scored_opportunities),
            "total_value": sum(opp['total_value'] for opp in scored_opportunities),
            "average_score": round(np.mean([opp['score'] for opp in scored_opportunities]), 2) if scored_opportunities else 0,
            "opportunities": scored_opportunities,
            "scoring_factors": {"similar_opportunities": 1.0},  # Simplified to single factor
            "opportunity_table": {
                "headers": ["Opportunity", "Score", "Risk", "Value", "Days Open", "Key Insights"],
                "rows": table_rows
            }
        }

def analyze_opportunities(file_path: str, date_range: str = 'all') -> Dict[str, Any]:
    """
    Main analysis function to process sales opportunity data
    """
    logger.info(f"Starting to read CSV file: {file_path}")
    try:
        data = pd.read_csv(file_path)
        logger.info(f"Successfully read CSV file with {len(data)} rows and {len(data.columns)} columns")
        logger.info(f"Columns in CSV: {data.columns.tolist()}")
        logger.info(f"Data types:\n{data.dtypes}")
        logger.info(f"Sample of data:\n{data.head()}")
        
        if data.empty:
            logger.error("CSV file is empty")
            raise ValueError("The uploaded CSV file is empty")
            
    except pd.errors.EmptyDataError:
        logger.error("CSV file is empty")
        raise ValueError("The uploaded CSV file is empty")
    except Exception as e:
        logger.error(f"Error reading CSV file: {str(e)}")
        raise

    try:
        logger.info("Initializing SalesOpportunityAnalyzer")
        analyzer = SalesOpportunityAnalyzer(data, date_range)
        
        logger.info("Calculating core metrics")
        core_metrics = analyzer.calculate_core_metrics()
        logger.info(f"Core metrics calculated: {core_metrics}")
        
        logger.info("Analyzing segment performance")
        segment_performance = analyzer.segment_performance()
        
        logger.info("Analyzing pipeline health")
        pipeline_health = analyzer.pipeline_health_analysis()
        
        logger.info("Analyzing loss patterns")
        loss_analysis = analyzer.analyze_loss_patterns()
        
        logger.info("Analyzing win patterns")
        win_analysis = analyzer.analyze_win_patterns()
        
        logger.info("Scoring open opportunities")
        open_opportunities = analyzer.score_open_opportunities()
        
        logger.info("Analysis completed successfully")
        results = {
            "Core Metrics": core_metrics,
            "Segment Performance": segment_performance,
            "Pipeline Health": pipeline_health,
            "Loss Analysis": loss_analysis,
            "Win Analysis": win_analysis,
            "Score Open Opportunities": open_opportunities
        }
        
        # Convert all numpy types to Python native types before returning
        return convert_numpy_types(results)
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        logger.error(f"Error traceback: {traceback.format_exc()}")
        raise