import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from typing import Dict, Any
from .analysis import SalesOpportunityAnalyzer

class SalesVisualization:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.layout_template = {
            'margin': {'t': 30, 'l': 40, 'r': 40, 'b': 40},
            'font': {'size': 10},
            'showlegend': True
        }
    
    def win_rate_by_type(self) -> tuple[str | None, dict[str, bool]]:
        """
        Generate win rate visualization by Type
        """
        type_win_rates = self.data.groupby('Type').agg({
            'Stage': lambda x: (x == 'Won').mean(),
            'Total ACV': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=type_win_rates['Type'],
            y=type_win_rates['Stage'],
            name='Win Rate',
            hovertemplate='%{y:.1%}<extra></extra>'
        ))
        
        fig.update_layout(
            **self.layout_template,
            yaxis_tickformat=',.0%',
            yaxis_title='Win Rate',
            xaxis_title='Type',
            dragmode=False,  # Disable drag interactions
        )
        
        # Return with config to remove modebar and disable all interactions
        return fig.to_json(), {
            'displayModeBar': False,  # Hide the modebar completely
            'staticPlot': True,       # Make the plot static (no interactions)
            'responsive': True        # Keep the plot responsive to container size
        }
    
    def trend_analysis(self) -> Dict[str, Any]:
        """
        Create trend visualizations
        """
        df = self.data.copy()
        df['Created Date'] = pd.to_datetime(df['Created Date'])
        df.set_index('Created Date', inplace=True)
        
        # Determine the resampling frequency based on date range
        date_range = df.index.max() - df.index.min()
        if date_range.days > 730:  # More than 2 years
            freq = 'Y'
            date_format = '%Y'
        elif date_range.days > 365:  # More than 1 year
            freq = '6M'
            date_format = '%b %Y'
        else:
            freq = 'M'
            date_format = '%b %Y'
        
        # Resample and aggregate data
        monthly_data = df.resample(freq).agg({
            'Total ACV': ['sum', 'mean'],
            'Opportunity Name': 'count',
            'Stage': lambda x: (x == 'Won').mean() * 100
        })
        
        monthly_data.columns = ['Total Volume', 'Average Deal Size', 'Number of Deals', 'Win Rate']
        dates = pd.to_datetime(monthly_data.index).strftime(date_format)
        
        # Create Win Rate Chart
        win_rate_fig = go.Figure()
        win_rate_fig.add_trace(go.Scatter(
            x=dates,
            y=monthly_data['Win Rate'],
            name='Win Rate',
            line=dict(color='rgb(34, 197, 94)')
        ))
        
        win_rate_layout = {
            **self.layout_template,
            'title': 'Win Rate Trend',
            'yaxis': dict(
                title='Win Rate (%)',
                tickformat=',.1f',
                range=[0, 100],
                showgrid=True
            ),
            'xaxis': dict(
                tickangle=45,
                showgrid=False,
                tickmode='array',
                ticktext=dates,
                tickvals=dates
            ),
            'height': 300,
            'margin': dict(b=100, r=40),  # Increased bottom margin
            'legend': dict(
                orientation="h",
                yanchor="bottom",
                y=-1,  # Moved down from -0.4 to -0.5
                xanchor="center",
                x=0.5
            )
        }
        win_rate_fig.update_layout(**win_rate_layout)
        
        # Create Volume and Deals Chart
        volume_fig = go.Figure()
        volume_fig.add_trace(go.Scatter(
            x=dates,
            y=monthly_data['Number of Deals'],
            name='Number of Deals',
            line=dict(color='rgb(99, 102, 241)')
        ))
        
        volume_fig.add_trace(go.Scatter(
            x=dates,
            y=monthly_data['Average Deal Size'],
            name='Average Deal Size',
            yaxis='y2',
            line=dict(color='rgb(59, 130, 246)')
        ))
        
        volume_layout = {
            **self.layout_template,
            'title': 'Volume Trends',
            'yaxis': dict(
                title='Number of Deals',
                showgrid=True
            ),
            'yaxis2': dict(
                title='Average Deal Size ($)',
                overlaying='y',
                side='right',
                showgrid=False,
                tickformat='$,.0f'
            ),
            'xaxis': dict(
                tickangle=45,
                showgrid=False,
                tickmode='array',
                ticktext=dates,
                tickvals=dates
            ),
            'height': 300,
            'margin': dict(b=100, r=40),  # Increased bottom margin
            'legend': dict(
                orientation="h",
                yanchor="bottom",
                y=-1,  # Moved down from -0.4 to -0.5
                xanchor="center",
                x=0.5
            )
        }
        volume_fig.update_layout(**volume_layout)
        
        return {
            'win_rate': win_rate_fig.to_json(),
            'volume': volume_fig.to_json()
        }

def generate_visualizations(file_path: str, date_range: str = 'all') -> Dict[str, Any]:
    """
    Generate all visualizations with date filtering
    """
    data = pd.read_csv(file_path)
    analyzer = SalesOpportunityAnalyzer(data, date_range)  # This will apply the date filter
    visualizer = SalesVisualization(analyzer.data)  # Pass the filtered data
    
    # Get plot data and config
    win_rates_data, win_rates_config = visualizer.win_rate_by_type()
    trends_data = visualizer.trend_analysis()
    
    plot_config = {
        'displayModeBar': False,
        'staticPlot': False,
        'responsive': True
    }
    
    return {
        "Win Rates by Type": {
            "data": win_rates_data,
            "config": win_rates_config
        },
        "Win Rate Trend": {
            "data": trends_data['win_rate'],
            "config": plot_config
        },
        "Volume Trend": {
            "data": trends_data['volume'],
            "config": plot_config
        }
    }
