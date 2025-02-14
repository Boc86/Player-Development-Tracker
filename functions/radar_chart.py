import plotly.express as px
import pandas as pd

def radar_chart(data, title):
    df = pd.DataFrame(data)
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    
    # Add target line at value 5
    target_theta = df['theta'].tolist() + [df['theta'].iloc[0]]  # Add first point to end
    fig.add_trace(
        dict(
            type='scatterpolar',
            r=[5] * (len(df['theta']) + 1),  # Add extra point to close the loop
            theta=target_theta,
            mode='lines',
            line_color='red',
            name='Target',
            line_dash='dot'  # Make it dotted for better visibility
        )
    )
    
    # Add markers with text labels
    fig.add_trace(
        dict(
            type='scatterpolar',
            r=df['r'],
            theta=df['theta'],
            mode='markers+text',
            text=df['r'].round(1),  # Show rounded values
            textposition='middle center',
            showlegend=False,
        )
    )

    fig.update_layout(
        showlegend=False,
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 10]
            )
        ),
    )
    return fig