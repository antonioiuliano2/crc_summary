import pandas as pd
import numpy as np

dftot = pd.read_csv("/home/iuliano/CRC_monitoring/crc_summary/CRCNetwork_status_report.csv", index_col="Time")

dfsorted = dftot.sort_index()

dfsorted.to_csv("/home/iuliano/CRC_monitoring/crc_summary/CRCNetwork_status_report_sorted.csv")
