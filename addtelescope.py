import pandas as pd
import numpy as np

newport = "7733"

df = pd.read_csv("/home/antonio/OCRA/CRC_monitoring/crc_summary/CRCNetwork_status_report.csv", index_col="Time")
df[newport] = 0

df_1 = pd.read_csv("/home/antonio/OCRA/CRC_monitoring/daily_summaries/2025-05-05.csv", index_col="Time")
df_2 = pd.read_csv("/home/antonio/OCRA/CRC_monitoring/daily_summaries/2025-05-06.csv", index_col="Time")

dftot = pd.concat([df,df_1,df_2],axis=0)

dftot.to_csv("/home/antonio/OCRA/CRC_monitoring/crc_summary/CRCNetwork_status_report_updated.csv")

