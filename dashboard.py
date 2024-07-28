import streamlit as st
import pandas as pd
import os
import plotly.express as px
import warnings
import plotly.graph_objects as go

warnings.filterwarnings('ignore')

st.set_page_config(page_title="TransactionAnalysis!!",page_icon=":bar_chart:",layout="wide")
st.title(":bar_chart: Transaction Monitoring")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
 os.chdir(r"G:\Upay")
df = pd.read_csv("today27.csv", encoding = "ISO-8859-1")

col1, col2=st.columns((2))
df["txn_date"]=pd.to_datetime(df["txn_date"])

# Getting the min and max date 
startDate = pd.to_datetime(df["txn_date"]).min()
endDate = pd.to_datetime(df["txn_date"]).max()
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["txn_date"] >= date1) & (df["txn_date"] <= date2)].copy()











#create transactio_type filter
st.sidebar.header('Choose Your Filter:')
transaction_type=st.sidebar.multiselect('Pick Your Transaction Type', df['transaction_type'].unique())
if not transaction_type:
   df2=df.copy()
else:
   df2=df[df['transaction_type'].isin(transaction_type)]   


#create payment for filter
payment_for = st.sidebar.multiselect("Pick the type of payment_for", df2["payment_for"].unique())
if not payment_for:
    df3 = df2.copy()
else:
    df3 = df2[df2["payment_for"].isin(payment_for)]

if not transaction_type and not payment_for:
    filtered_df = df
elif transaction_type and payment_for:
    filtered_df = df3[df["transaction_type"].isin(transaction_type) & df3["payment_for"].isin(payment_for)]
else:
    filtered_df = df3[df3["transaction_type"].isin(transaction_type) & df3["payment_for"].isin(payment_for)]   

status_df = filtered_df.groupby(by = ["status"], as_index = False)["total_transaction_count"].sum()

############################################################################################################
col1,col2=st.columns((2))
with col1:
    st.subheader("Transaction Type wise Refund Distribution")

    refunded_df = df[df["status"] == "refunded"]
   
    grouped_refunded_df = refunded_df.groupby("transaction_type")["total_transaction_count"].sum().reset_index()
   
    fig = px.bar(
        grouped_refunded_df, 
        x="transaction_type", 
        y="total_transaction_count", 
        text=['{:,.2f}'.format(x) for x in grouped_refunded_df["total_transaction_count"]],
        template="seaborn",
        color_discrete_sequence=["yellow"]
    )
    st.plotly_chart(fig, use_container_width=True, height=200)
    with st.expander("Refund_ViewData"):
        st.write(grouped_refunded_df.style.background_gradient(cmap="Blues"))
        csv = grouped_refunded_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "refund.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
with col2:
    st.subheader("Status wise Transaction count")
    fig = px.bar(
        status_df, 
        x="status", 
        y="total_transaction_count", 
        text=['{:,.2f}'.format(x) for x in status_df["total_transaction_count"]],
        template="seaborn",
        color_discrete_sequence=["blue"]
    )
    st.plotly_chart(fig, use_container_width=True, height=200)
    with st.expander("Status Wise ViewData"):
        region = filtered_df.groupby(by = "status", as_index = False)["total_transaction_count"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "statuswise.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')    
with col1:
    st.subheader("Transaction Type wise Failed Distribution")

    refunded_df = df[df["status"] == "failed"]
   
    grouped_refunded_df = refunded_df.groupby("transaction_type")["total_transaction_count"].sum().reset_index()
   
    fig = px.bar(
        grouped_refunded_df, 
        x="transaction_type", 
        y="total_transaction_count", 
        text=['{:,.2f}'.format(x) for x in grouped_refunded_df["total_transaction_count"]],
        template="seaborn",
        color_discrete_sequence=["blue"]
    )
    st.plotly_chart(fig, use_container_width=True, height=200)
    with st.expander("Failed_ViewData"):
        st.write(grouped_refunded_df.style.background_gradient(cmap="Blues"))
        csv = grouped_refunded_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "failed.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')


with col2:
    st.subheader("Transaction Type wise Vendor Failed Distribution")

    refunded_df = df[df["status"] == "vendor_failed"]
   
    grouped_refunded_df = refunded_df.groupby("transaction_type")["total_transaction_count"].sum().reset_index()
   
    fig = px.bar(
        grouped_refunded_df, 
        x="transaction_type", 
        y="total_transaction_count", 
        text=['{:,.2f}'.format(x) for x in grouped_refunded_df["total_transaction_count"]],
        template="seaborn",
        color_discrete_sequence=["yellow"]
    )
    st.plotly_chart(fig, use_container_width=True, height=200)
    with st.expander("Vendor Failed_ViewData"):
        st.write(grouped_refunded_df.style.background_gradient(cmap="Blues"))
        csv = grouped_refunded_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Vendor failed.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
    


col1,col2,col3=st.columns((3))

with col1:
    st.subheader("Transaction Type wise Refund Distribution")
    
    # Filter the DataFrame to include only refunded transactions
    refunded_df = filtered_df[filtered_df["status"] == "refunded"]
    
    # Create the pie chart with the filtered data
    fig = px.pie(refunded_df, values="total_transaction_count", names="payment_for", hole=0.4)
    fig.update_traces(text=refunded_df["payment_for"], textposition="outside")
    
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Refund_ViewData"):
        region = refunded_df.groupby(by = "payment_for", as_index = False)["total_transaction_count"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "refunded.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file',key='download_refund_data')

with col2:
    st.subheader("Transaction Type wise Failed Distribution")
    
    # Filter the DataFrame to include only refunded transactions
    failed_df = filtered_df[filtered_df["status"] == "failed"]
    
    # Create the pie chart with the filtered data
    fig = px.pie(failed_df, values="total_transaction_count", names="payment_for", hole=0.5)
    fig.update_traces(text=failed_df["payment_for"], textposition="outside")
    
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("failed_ViewData"):
        region = failed_df.groupby(by = "payment_for", as_index = False)["total_transaction_count"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "failed.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file',key='download_failed_data')
with col3:
    st.subheader("Transaction Type wise Vendor_Failed Distribution")
    
    # Filter the DataFrame to include only refunded transactions
    vendor_failed_df = filtered_df[filtered_df["status"] == "vendor_failed"]
    
    # Create the pie chart with the filtered data
    fig = px.pie(vendor_failed_df, values="total_transaction_count", names="payment_for", hole=0.5)
    fig.update_traces(text=vendor_failed_df["payment_for"], textposition="outside")
    
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("vendor_failed_ViewData"):
        region = vendor_failed_df.groupby(by = "payment_for", as_index = False)["total_transaction_count"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "vendor_failed.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file',key='download_v_failed_data')
        
 ##timeseries


# Create 'day_month' as a datetime column
filtered_df["day_month"] = filtered_df["txn_date"].dt.to_period("D").dt.to_timestamp()

# Group by and sum for all transactions
linechart_all = (filtered_df
                 .groupby(filtered_df["day_month"].dt.strftime("%Y-%m-%d"))
                 ["total_transaction_count"]
                 .sum()
                 .reset_index())
linechart_all["day_month"] = pd.to_datetime(linechart_all["day_month"])
linechart_all.sort_values("day_month", inplace=True)

# Group by and sum for refunded transactions
refunded_df = filtered_df[filtered_df["status"] == "refunded"]
linechart_refunded = (refunded_df
                      .groupby(refunded_df["day_month"].dt.strftime("%Y-%m-%d"))
                      ["total_transaction_count"]
                      .sum()
                      .reset_index())
linechart_refunded["day_month"] = pd.to_datetime(linechart_refunded["day_month"])
linechart_refunded.sort_values("day_month", inplace=True)

# Merge the two DataFrames on the 'day_month' column
combined_linechart = pd.merge(linechart_all, linechart_refunded, on="day_month", how="outer", suffixes=('_all', '_refunded'))
combined_linechart.fillna(0, inplace=True)  # Fill NaN values with 0

# Create the line chart with Plotly
fig = go.Figure()

# Add the first trace for all transactions
fig.add_trace(go.Scatter(x=combined_linechart["day_month"], y=combined_linechart["total_transaction_count_all"],
                         mode='lines', name='All Transactions', line=dict(color='blue')))

# Add the second trace for refunded transactions
fig.add_trace(go.Scatter(x=combined_linechart["day_month"], y=combined_linechart["total_transaction_count_refunded"],
                         mode='lines', name='Refunded Transactions', line=dict(color='orange')))

# Update layout
fig.update_layout(
    title='Time Series Analysis',
    xaxis_title='Date',
    yaxis_title='Total Transaction Count',
    template='gridon',
    height=500,
    width=1000
)

# Display the line chart in Streamlit
st.subheader('Time Series Analysis')
st.plotly_chart(fig, use_container_width=True)

# Display the data and download button within an expander
with st.expander("View Data of TimeSeries:"):
    st.write(combined_linechart.T.style.background_gradient(cmap="Blues"))
    csv_combined = combined_linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Combined Data', data=csv_combined, file_name="TimeSeries_Combined.csv", mime='text/csv')
