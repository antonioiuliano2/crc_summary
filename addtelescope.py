import pandas as pd
import numpy as np

newport = "7764"

dftot = pd.read_csv("/home/iuliano/CRC_monitoring/crc_summary/CRCNetwork_status_report.csv", index_col="Time")
dftot[newport] = 0

dftot.to_csv("/home/iuliano/CRC_monitoring/crc_summary/CRCNetwork_status_report_updated.csv")

