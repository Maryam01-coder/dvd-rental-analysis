import pandas as pd
import plotly.express as px 
import streamlit as st

#page set up
st.set_page_config(
    page_title="DVD Rental Analysis",
    page_icon="🎬",
    layout="wide"
)

# @st.cache_data
def load_dataset():
    try:
        f_df = pd.read_csv("cleaned_film_dataset.csv")
        c_df = pd.read_csv("cleaned_customer_dataset.csv")
        t_df = pd.read_csv("cleaned_time_trends.csv")
        s_df = pd.read_csv("cleaned_staff_dataset.csv")
        return f_df, c_df, t_df, s_df
    except FileNotFoundError as e:
        st.warning(f"An Error occured: {e}")

# =========================
# PAGE FUNCTIONS
# =========================
# Reusable return button for analysis pages
def back_to_overview():
    if st.sidebar.button("← Back to Overview"):
        st.session_state.page = "Overview"
        st.rerun()

def format_number(value):
    if value >= 1000000:
        return f"${value / 1000000:.1f}M"
    elif value >= 1000:
        return f"${value / 1000:.1f}K"
    else:
        return f"${value:,.0f}"

def nav():
    pages = [
            "Overview",
            "Film & Category",
            "Customers",
            "Time Trends",
            "Staff & Store",
            "Findings & Recommendations"
    ]
    
    selected = st.sidebar.selectbox(
        "All Pages",
        pages,
        index=pages.index(st.session_state.page),
        key="overview_nav"
        )
    
    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()

def show_overview(f_df, c_df, t_df, s_df):
    # Overview page
    nav()

    st.title("DVD Rental Dashboard")

    st.markdown("---")

    # Overview content
    st.subheader("Overview")

    st.write('''This analysis evaluates the DVD rental business across film performance, 
    customer behavior, rental trends, staff revenue and geographical markets. 
    The notebook records $61,312.04 in total rental revenue, approximately 4.97 days in average film rental duration, 
    and 599 customers in the analyzed customer dataset.''')

    #tables for each df
    st.header("Dataset Overview")

    st.subheader("Film Dataset")
    st.dataframe(f_df, use_container_width=True)

    st.subheader("Customer Dataset")
    st.dataframe(c_df, use_container_width=True)

    st.subheader("Time Trends Dataset")
    st.dataframe(t_df, use_container_width=True)

    st.subheader("Staff Dataset")
    st.dataframe(s_df, use_container_width=True)

def show_revenue(f_df):
    back_to_overview()
    nav()

    st.title("Film and Revenue Analysis")

    # Page-specific sidebar filters
    st.sidebar.header("Filter")

    selected_category = st.sidebar.multiselect(
        "Select Category",
        options=f_df["category"].unique(),
        default=f_df["category"].unique(),
    )

    def filter_data(f_df, category):
        filtered_df = f_df[
            (f_df["category"].isin(category)) & 
            (f_df["category"].isin(category)) 
        ]
        return filtered_df
    
    filtered_df = filter_data(f_df, selected_category)  

    # Main page content
    st.markdown("---")    
    # metrics/kpi
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Films", len(filtered_df))

    with col2:
        total_rentals = filtered_df["total_rentals"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Rentals", f"{total_rentals:,.0f}")

    with col3:
        total_rev = filtered_df["total_rental_revenue"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Revenue", format_number(total_rev))

    with col4:
        most_common_category = filtered_df["category"].value_counts().idxmax() if len(filtered_df) > 0 else 0
        st.metric("Most Common Category", f"{most_common_category}")

    # charts
    if len(filtered_df) == 0:
        st.warning('No Filter Selected. Please Adjust Your Selection.')
        return

    st.subheader('Top 10 Films by Rentals')
    top_film_rentals = filtered_df.groupby("film_title")["total_rentals"].sum().sort_values(ascending=False).head(10)
    fig1 = px.bar(
        x=top_film_rentals.values,
        y=top_film_rentals.index
    )
    fig1.update_layout(
        xaxis_title='Number of Rentals',
        yaxis_title='Film'
    )
    st.plotly_chart(fig1, width='stretch')

    st.subheader('Top 10 Films by Revenue')
    top_film_rentals = filtered_df.groupby("film_title")["total_rental_revenue"].sum().sort_values(ascending=False).head(10)
    fig2 = px.bar(
        x=top_film_rentals.index,
        y=top_film_rentals.values
    )
    fig2.update_layout(
        xaxis_title='Film',
        yaxis_title='Revenue'
    )
    st.plotly_chart(fig2, width='stretch')
    
    st.subheader('Distribution of Categories')
    category_count = filtered_df["category"].value_counts()
    fig = px.pie(
        values=category_count.values, 
        names=category_count.index, 
    )
    st.plotly_chart(fig, width='stretch')

    st.subheader('Distribution of Categories by Rentals')
    top_cat_rentals = filtered_df.groupby("category")["total_rentals"].sum().sort_values(ascending=False).head(10)
    fig3 = px.bar(
        x=top_cat_rentals.values,
        y=top_cat_rentals.index
    )
    fig3.update_layout(
        xaxis_title='Number of Rentals',
        yaxis_title='Category'
    )
    st.plotly_chart(fig3, width='stretch')

    st.subheader('Distribution of Categories by Revenue')
    top_cat_rev = filtered_df.groupby("category")["total_rental_revenue"].sum().sort_values(ascending=False).head(10)
    fig4 = px.bar(
        x=top_cat_rev.index,
        y=top_cat_rev.values
    )
    fig4.update_layout(
        xaxis_title='Category',
        yaxis_title='Revenue'
    )
    st.plotly_chart(fig4, width='stretch')

def show_customers(c_df):
    back_to_overview()
    nav()

    st.title("Customer Analysis")
    st.markdown("---")

    # Customer-specific filters
    st.sidebar.header("Filters")

    selected_category = st.sidebar.multiselect(
        "Select Category",
        options=c_df["top_category"].unique(),
        default=c_df["top_category"].unique(),
    )

    selected_city = st.sidebar.multiselect(
        "Select City",
        options=c_df["city"].unique(),
        default=c_df["city"].unique(),
    )

    selected_country = st.sidebar.multiselect(
        "Select Country",
        options=c_df["country"].unique(),
        default=c_df["country"].unique(),
    )
    
    def filter_data(c_df, category, city, country):
        filtered_df = c_df[
            (c_df["top_category"].isin(category)) & 
            (c_df["top_category"].isin(category)) &
            (c_df["city"].isin(city)) & 
            (c_df["city"].isin(city)) &
            (c_df["country"].isin(country)) & 
            (c_df["country"].isin(country))
        ]
        return filtered_df
    
    filtered_df = filter_data(c_df, selected_category, selected_city, selected_country)

    # METRICS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Customers", len(filtered_df))

    with col2:
        total_rentals = filtered_df["total_rentals"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Rentals", f"{total_rentals:,.0f}")

    with col3:
        total_spending = filtered_df["total_amount_spent"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Spendings", format_number(total_spending))

    with col4:
        avg_spending = filtered_df["total_amount_spent"].mean() if len(filtered_df) > 0 else 0
        st.metric("Average Spending", format_number(avg_spending))

    # charts
    if len(filtered_df) == 0:
        st.warning('No Filter Selected. Please Adjust Your Selection.')
        return

    st.subheader('Top 15 Customers by Rentals')
    top_cus_rentals = filtered_df.groupby("customer_name")["total_rentals"].sum().sort_values(ascending=False).head(15)
    fig1 = px.bar(
        x=top_cus_rentals.values,
        y=top_cus_rentals.index
    )
    fig1.update_layout(
        xaxis_title='Number of Rentals',
        yaxis_title='Customers'
    )
    st.plotly_chart(fig1, width='stretch')

    st.subheader('Top 15 Customers by Spendings')
    top_cus_rev = filtered_df.groupby("customer_name")["total_amount_spent"].sum().sort_values(ascending=False).head(15)
    fig2 = px.bar(
        x=top_cus_rev.index,
        y=top_cus_rev.values
    )
    fig2.update_layout(
        xaxis_title='Customers',
        yaxis_title='Spendings'
    )
    st.plotly_chart(fig2, width='stretch')

    st.subheader('Distribution of Customer Spendings')
    cust_spend = filtered_df.groupby("customer_name")["total_amount_spent"].sum()
    fig3 = px.histogram(
        x=cust_spend.values,
        nbins=10
    )
    fig3.update_layout(
        xaxis_title='Customer Spendings',
        yaxis_title='Customer Count'
    )
    fig3.update_traces(
    marker_line_color="white",
    marker_line_width=2
    )
    st.plotly_chart(fig3, width='stretch')

    st.subheader('Top 10 Country by Revenue')
    top_country = filtered_df.groupby("country")["total_amount_spent"].sum().sort_values(ascending=False).head(10)
    fig4 = px.bar(
        x=top_country.index,
        y=top_country.values
    )
    fig4.update_layout(
        xaxis_title='Country',
        yaxis_title='Revenue'
    )
    st.plotly_chart(fig4, width='stretch')

    st.subheader('Top 10 Country by Rentals')
    top_country = filtered_df.groupby("country")["total_rentals"].sum().sort_values(ascending=False).head(10)
    fig5 = px.bar(
        x=top_country.index,
        y=top_country.values
    )
    fig5.update_layout(
        xaxis_title='Country',
        yaxis_title='Rentals'
    )
    st.plotly_chart(fig5, width='stretch')

def show_time(t_df):
    back_to_overview()
    nav()
    st.title("Time Trend Analysis")
    st.markdown("---")

    st.sidebar.header("Filter")

    selected_date = st.sidebar.selectbox(
        "Select Year",
        options=["All",  "2005", "2006"],
        index=0
    )

    def filter_data(s_df, selected_date):
        if selected_date != "All":
            selected_year = int(selected_date)
            s_df = s_df[
                s_df["rental_year"] == selected_year
            ]
        return s_df
    
    filtered_df = filter_data(t_df, selected_date)

    # metrics 
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        most_month = filtered_df.groupby("rental_month")["total_rentals"].sum().idxmax() if len(filtered_df) > 0 else 0
        st.metric("Month with Most Rental", most_month)

    with col2:
        total_rentals = filtered_df["total_rentals"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Rentals", f"{total_rentals:,.0f}")

    with col3:
        total_revenue = filtered_df["total_revenue"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Revenue", format_number(total_revenue))

    with col4:
        avg_rev = filtered_df["total_revenue"].mean() if len(filtered_df) > 0 else 0
        st.metric("Average Revenue", format_number(avg_rev))

    #charts
    st.subheader('Monthly Distribution of Rentals')
    filtered_df = filtered_df.iloc[::-1]
    
    fig1 = px.line(
        filtered_df,
        x="rental_month",
        y="total_rentals",
        labels={
            "rental_month": "Month",
            "value": "Total",
            "variable": "Metric"
        },
        markers=True
    )
    st.plotly_chart(fig1, width='stretch')

    st.subheader('Monthly Distribution of Revenue')    
    fig2 = px.line(
        filtered_df,
        x="rental_month",
        y="total_revenue",
        labels={
            "rental_month": "Month",
            "value": "Total",
            "variable": "Metric"
        },
        markers=True
    )
    st.plotly_chart(fig2, width='stretch')

    st.subheader('Monthly Customer Activity')    
    fig3 = px.line(
        filtered_df,
        x="rental_month",
        y="unique_customers",
        labels={
            "rental_month": "Month",
            "value": "Customers",
            "variable": "Metric"
        },
        markers=True
    )
    st.plotly_chart(fig3, width='stretch')


def show_staff(s_df):
    back_to_overview()
    nav()
    st.title("Store & Staff Performance")
    st.markdown("---")

    # Staff and store filters
    st.sidebar.header("Staff Filter")

    staff = st.sidebar.selectbox(
        "Staff Members",
        options=["All", "Jon Stephens", "Mike Hillyer"],
        index=0
    )
    def filter_data(s_df, selected_staff):
        if selected_staff != "All":
            s_df = s_df[
                s_df["staff_name"] == selected_staff
            ]
        return s_df

    filtered_df = filter_data(s_df, staff)

    # metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Staffs", filtered_df["staff_name"].nunique())

    with col2:
        total_rentals = filtered_df["total_rentals"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Rentals", f"{total_rentals:,.0f}")

    with col3:
        total_revenue = filtered_df["total_revenue"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Revenue", format_number(total_revenue))

    with col4:
        customer_s = filtered_df["unique_customers"].mean() if len(filtered_df) > 0 else 0
        st.metric("Customer Served", f"{customer_s:.0f}")

    #charts 
    st.subheader('Staff Revenue Perfomance')
    top_cus_rev = filtered_df.groupby("staff_name")["total_revenue"].sum()
    fig2 = px.bar(
        x=top_cus_rev.values,
        y=top_cus_rev.index
    )
    fig2.update_layout(
        xaxis_title='Revenue',
        yaxis_title='Staff'
    )
    st.plotly_chart(fig2, width='stretch')

    st.subheader('Total Rentals Processed by Staff')
    top_cus_rev = filtered_df.groupby("staff_name")["total_rentals"].sum()
    fig3 = px.bar(
        x=top_cus_rev.values,
        y=top_cus_rev.index
    )
    fig3.update_layout(
        xaxis_title='Rentals',
        yaxis_title='Staff'
    )
    st.plotly_chart(fig3, width='stretch')

    st.subheader('Average Rental Recorded by Staff')
    top_cus_rev = filtered_df.groupby("staff_name")["average_rentals_per_day"].sum()
    fig3 = px.bar(
        x=top_cus_rev.values,
        y=top_cus_rev.index
    )
    fig3.update_layout(
        xaxis_title='Rentals',
        yaxis_title='Staff'
    )
    st.plotly_chart(fig3, width='stretch')


def show_findings():
    back_to_overview()
    nav()
    st.title("Findings & Recommendations")
    st.markdown("---")

    with open("findings.md", "r", encoding="utf-8") as file:
        findings = file.read()
    st.markdown(findings)

# =========================
# MAIN FUNCTION
# =========================

def main():
    f_df, c_df, t_df, s_df = load_dataset()

    # Initialize current page
    if "page" not in st.session_state:
        st.session_state.page = "Overview"

    # Page routing
    if st.session_state.page == "Overview":
        show_overview(f_df, c_df, t_df, s_df)

    elif st.session_state.page == "Film & Category":
        show_revenue(f_df)

    elif st.session_state.page == "Customers":
        show_customers(c_df)

    elif st.session_state.page == "Time Trends":
        show_time(t_df)

    elif st.session_state.page == "Staff & Store":
        show_staff(s_df)

    elif st.session_state.page == "Findings & Recommendations":
        show_findings()

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    main()