import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def parse_log_file(file_path):
    # Lists to store parsed data
    timestamps = []
    levels = []
    loggers = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into components
            parts = line.split(' - ')
            if len(parts) >= 4:
                timestamp_str = parts[0]
                level = parts[2]
                message = parts[3]
                
                # Extract logger number
                logger_num = message.strip().split()[-1]
                
                # Convert timestamp string to datetime
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                
                timestamps.append(timestamp)
                levels.append(level)
                loggers.append(logger_num)
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'level': levels,
        'logger': loggers
    })
    
    return df

def plot_log_metrics(df):
    # Create figure with subplots (2x2 grid)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Process data for logger1
    logger1_data = df[df['logger'] == 'logger1'].copy()
    logger1_counts = logger1_data.groupby(['timestamp', 'level']).size().unstack(fill_value=0)
    logger1_counts_sum = logger1_data.groupby(['timestamp', 'level']).size().unstack(fill_value=0).cumsum()

    # Process data for logger2
    logger2_data = df[df['logger'] == 'logger2'].copy()
    logger2_counts = logger2_data.groupby(['timestamp', 'level']).size().unstack(fill_value=0)
    logger2_counts_sum = logger2_data.groupby(['timestamp', 'level']).size().unstack(fill_value=0).cumsum()

    # Plot logger1 regular counts
    
    logger1_counts.plot(ax=ax1,linestyle='', marker='o',  markersize=5,alpha=0.6)
    ax1.set_title('Logger1 Metrics Over Time')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Count')
    ax1.legend(title='Level')
    ax1.grid(True)
    
    # Plot logger2 regular counts
    logger2_counts.plot(ax=ax2,linestyle='', marker='o',  markersize=5,alpha=0.6)
    ax2.set_title('Logger2 Metrics Over Time')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Count')
    ax2.legend(title='Level')
    ax2.grid(True)

    # Plot logger1 cumulative counts
    logger1_counts_sum.plot(ax=ax3, linestyle='', marker='o',  markersize=5,alpha=0.6)
    ax3.set_title('Logger1 Cumulative Metrics Over Time')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Cumulative Count')
    ax3.legend(title='Level')
    ax3.grid(True)
    
    # Plot logger2 cumulative counts
    logger2_counts_sum.plot(ax=ax4, linestyle='', marker='o',  markersize=5,alpha=0.6)
    ax4.set_title('Logger2 Cumulative Metrics Over Time')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Cumulative Count')
    ax4.legend(title='Level')
    ax4.grid(True)
    
    plt.tight_layout()
    plt.show()

# Usage
if __name__ == "__main__":
    log_file_path = "shared_output1.log"  # Replace with your log file path
    df = parse_log_file(log_file_path)
    plot_log_metrics(df)