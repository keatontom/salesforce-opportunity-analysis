import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List

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
        self.data = data
        self.validate_columns()
        self.prepare_data()
        self.filter_by_date_range(date_range)
    
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
        
        # Add missing columns with default values
        for col, dtype in required_columns.items():
            if col not in self.data.columns:
                if dtype == 'object':
                    self.data[col] = 'Unknown'
                elif dtype.startswith('float'):
                    self.data[col] = 0.0
                elif dtype.startswith('datetime'):
                    self.data[col] = pd.Timestamp.now()
                print(f"Warning: Added missing column '{col}' with default values")

    def prepare_data(self):
        """
        Preprocess and transform the raw data
        """
        # Convert date columns, handling potential format issues
        for date_col in ['Created Date', 'Close Date']:
            try:
                self.data[date_col] = pd.to_datetime(self.data[date_col]) # type: ignore
            except:
                print(f"Warning: Could not parse {date_col}, using current date")
                self.data[date_col] = pd.Timestamp.now()
        
        # Calculate time to close
        self.data['Time_To_Close'] = (self.data['Close Date'] - self.data['Created Date']).dt.days
        
    def filter_by_date_range(self, date_range: str):
        """
        Filter data based on date range
        """
        if date_range == 'all':
            return
        
        today = datetime.now()
        current_year = today.year
        
        if date_range == 'last_year':
            start_date = datetime(current_year - 1, 1, 1)
            end_date = datetime(current_year - 1, 12, 31)
            self.data = self.data[
                (self.data['Created Date'] >= start_date) & 
                (self.data['Created Date'] <= end_date)
            ]
        elif date_range == 'ytd':
            start_date = datetime(current_year, 1, 1)
            self.data = self.data[self.data['Created Date'] >= start_date]
        else:
            # Handle quarters
            quarter_map = {
                'q1': (1, 3),
                'q2': (4, 6),
                'q3': (7, 9),
                'q4': (10, 12)
            }
            if date_range in quarter_map:
                start_month, end_month = quarter_map[date_range]
                start_date = datetime(current_year, start_month, 1)
                if end_month == 12:
                    end_date = datetime(current_year, end_month, 31)
                else:
                    end_date = datetime(current_year, end_month + 1, 1) - timedelta(days=1)
                
                self.data = self.data[
                    (self.data['Created Date'] >= start_date) & 
                    (self.data['Created Date'] <= end_date)
                ]
    
    def calculate_core_metrics(self) -> Dict[str, Any]:
        """
        Calculate core sales metrics
        """
        return {
            "Total Volume": round(self.data['Total ACV'].sum(), 2),
            "Average Deal Size": round(self.data['Total ACV'].mean(), 2),
            "Win Rate": round(len(self.data[self.data['Stage'] == 'Won']) / len(self.data) * 100, 2),
            "Average Time to Close": round(self.data['Time_To_Close'].mean(), 2),
            "Number of Opportunities": len(self.data)
        }
    
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
            'Stage': lambda x: (x == 'Won').mean() * 100  # Convert to percentage
        }).reset_index()
        account_performance.columns = ['Account Name', 'Total Volume', 'Avg Deal Size', 'Win Rate']
        account_performance['Total Volume'] = account_performance['Total Volume'].round(2)
        account_performance['Avg Deal Size'] = account_performance['Avg Deal Size'].round(2)
        account_performance['Win Rate'] = account_performance['Win Rate'].round(2)
        
        # Performance by Type with opportunities
        type_performance = []
        for type_name in self.data['Type'].unique():
            type_data = self.data[self.data['Type'] == type_name]
            type_perf = {
                'Type': type_name,
                'Total Volume': round(type_data['Total ACV'].sum(), 2),
                'Avg Deal Size': round(type_data['Total ACV'].mean(), 2),
                'Win Rate': round(len(type_data[type_data['Stage'] == 'Won']) / len(type_data) * 100, 2),
                'opportunities': type_data[[
                    'Account Name', 'Opportunity Name', 'Total ACV', 'Created Date', 'Type'
                ]].to_dict(orient='records')
            }
            type_performance.append(type_perf)
        
        # Performance by Practice Area - splitting semicolon-separated areas
        # Handle missing or invalid values by excluding them
        valid_areas = self.data['Law Firm Practice Area'].notna()
        
        # Create exploded dataframe only for valid practice areas
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
        
        # Group by individual practice areas
        practice_performance = practice_areas_exploded.groupby('Practice Area').agg({
            'Total ACV': ['sum', 'mean'],
            'Stage': lambda x: (x == 'Won').mean() * 100  # Convert to percentage
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
        stage_distribution = {}
        for stage in self.data['Stage'].unique():
            stage_data = self.data[self.data['Stage'] == stage]
            count = len(stage_data)
            
            stage_distribution[stage] = {
                'percentage': float(count / len(self.data)),
                'count': int(count)
            }
        
        # Lost opportunity analysis
        lost_reasons = self.data[self.data['Stage'] == 'Lost']['Closed Lost Reason'].value_counts()
        
        # Aging opportunities
        aging_opportunities = self.data.copy()
        aging_opportunities['Created Date'] = pd.to_datetime(aging_opportunities['Created Date'], utc=True)
        current_time = pd.Timestamp.now(tz='UTC')
        aging_opportunities['Days Open'] = (current_time - aging_opportunities['Created Date']).dt.days # type: ignore
        
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
            loss_rate = (count/total_lost*100)
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
                loss_rate = (lost_type / total_type) * 100
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
            "total_lost": len(lost_opps),
            "total_value_lost": lost_opps['Total ACV'].sum(),
            "avg_value_lost": lost_opps['Total ACV'].mean(),
            "avg_cycle_length": int(round(lost_opps['Time_To_Close'].mean())),
            "insights": [
                {
                    "category": "Practice Area Failures",
                    "finding": "\n".join(practice_summary),
                    "severity": "high"
                },
                {
                    "category": "Type Performance",
                    "finding": "\n".join(type_summary),
                    "severity": "high" if any(x['loss_rate'] > 75 for x in type_stats) else "medium"
                },
                {
                    "category": "Campaign Performance",
                    "finding": "\n".join(campaign_text) if campaign_text else "No significant campaign data available",
                    "severity": "medium"
                },
                {
                    "category": "Failure Reasons",
                    "finding": "\n".join(reason_summary),
                    "severity": "high"
                },
                {
                    "category": "Lawyer Count Distribution",
                    "finding": "\n".join(size_summary),
                    "severity": "medium"
                }
            ]
        }
    
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
        avg_cycle_length = int(round(won_opps['Time_To_Close'].mean()))  # Rounded to nearest day

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
                win_rate = (won_type / total_type) * 100
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

        won_opps['Campaign Category'] = won_opps['Primary Campaign Source'].apply(categorize_campaign)
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
        campaign_text = [item['text'] for item in campaign_summary[:3]]  # Take top 3

        return {
            "has_data": True,
            "total_won": total_won,
            "total_value_won": total_value_won,
            "avg_value_won": total_value_won / total_won if total_won > 0 else 0,
            "avg_cycle_length": avg_cycle_length,
            "insights": [
                {
                    "category": "Practice Area Successes",
                    "finding": "\n".join(practice_summary),
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
                    "finding": "\n".join(size_summary),
                    "severity": "medium"
                }
            ]
        }

def analyze_opportunities(file_path: str, date_range: str = 'all') -> Dict[str, Any]:
    """
    Main analysis function to process sales opportunity data
    """
    data = pd.read_csv(file_path)
    analyzer = SalesOpportunityAnalyzer(data, date_range)
    
    return {
        "Core Metrics": analyzer.calculate_core_metrics(),
        "Segment Performance": analyzer.segment_performance(),
        "Pipeline Health": analyzer.pipeline_health_analysis(),
        "Loss Analysis": analyzer.analyze_loss_patterns(),
        "Win Analysis": analyzer.analyze_win_patterns()
    }
