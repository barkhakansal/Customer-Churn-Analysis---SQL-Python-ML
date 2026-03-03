-- Churn Focused Analysis

-- What is the overall churn rate?

select cast(count( case when Customer_Status = 'Churned' then 1 end) * 100.0/ count(*) as decimal(10,2))
as churn_percentage from stg_Churn;

-- Which contract type has the highest churn rate?

select Contract, count(case when Customer_Status = 'Churned' then 1 end) as churned_customer,
cast(count( case when Customer_Status = 'Churned' then 1 end) * 100.0/ count(*) as decimal(10,2)) as churn_percentage
from stg_Churn
group by Contract;

-- Does gender impact churn?

select gender, count(case when Customer_Status = 'Churned' then 1 end) as churned_customer,
cast(count( case when Customer_Status = 'Churned' then 1 end) * 100.0/ count(*) as decimal(10,2)) as churn_percentage
from stg_Churn
group by gender;

-- Which states have the highest churn percentage?
select state, count(*) as total_customers, 
count(case when Customer_Status = 'Churned' then 1 end) as churned_customer,
cast(count( case when Customer_Status = 'Churned' then 1 end) * 100.0/ count(*) as decimal(10,2)) as churn_percentage
from stg_Churn
group by state
order by churn_percentage desc;

-- Do high-revenue customers churn more or less?

select 
	case when Total_Revenue < 1000 then 'Low Revenue'
		 when Total_Revenue between 1000 and 3000 then 'Medium Revenue'
		 else 'High Revenue'
	end as Revenue_Segmnent,
count(*) as total_customers, 
count(case when Customer_Status = 'Churned' then 1 end) as churned_customer,
cast(count( case when Customer_Status = 'Churned' then 1 end) * 100.0/ count(*) as decimal(10,2)) as churn_percentage
from stg_Churn
group by 
	case when Total_Revenue < 1000 then 'Low Revenue'
		 when Total_Revenue between 1000 and 3000 then 'Medium Revenue'
		 else 'High Revenue'
	end
order by churn_percentage desc;

-- Does tenure impact churn probability?

select 
	case when Tenure_in_Months < 12 then '0-1 Year'
		 when Tenure_in_Months between 12 and 24 then '1-2 Years'
		 else '2+ Years'
	end as Tenure_Segmnent,
count(*) as total_customers, 
count(case when Customer_Status = 'Churned' then 1 end) as churned_customer,
cast(count( case when Customer_Status = 'Churned' then 1 end) * 100.0/ count(*) as decimal(10,2)) as churn_percentage
from stg_Churn
group by 
	case when Tenure_in_Months < 12 then '0-1 Year'
		 when Tenure_in_Months between 12 and 24 then '1-2 Years'
		 else '2+ Years'
	end
order by churn_percentage desc;


-- Revenue Impact Analysis

-- revenue by customer status

select customer_status,cast(sum(Total_Revenue) as decimal(10,2)) as total_revenue
from stg_Churn
group by customer_status

-- revenue lost due to churn

select 
cast(sum(case when Customer_Status = 'Churned' then Total_Revenue else 0 end) as decimal(10,2)) as revenue_from_churned,
cast(sum(total_revenue) as decimal(10,2)) as total_revenue,
cast(sum(case when Customer_Status = 'Churned' then Total_Revenue else 0 end)* 100.0/ sum(total_revenue) as decimal(10,2))
as Percentage_Revenue_From_Churned
from stg_Churn

-- What is the average revenue per customer?

select cast(AVG(total_revenue) as decimal(10,2)) as AvgRevPerCustomer from stg_Churn

-- Do long-term contracts generate more revenue?

select contract, cast(sum(total_revenue) as decimal(10,2)) as total_revenue from stg_Churn
group by Contract

-- Which state generates highest revenue?

select state, cast(sum(total_revenue) as decimal(10,2)) as total_revenue from stg_Churn
group by state
order by sum(total_revenue) desc;

-- churn rate by state with ranking

select State, cast(count(case when Customer_Status = 'Churned' then 1 end)*100.0/ count(*) as decimal(10,2)) as churn_rate,
rank() over(order by  count(case when Customer_Status = 'Churned' then 1 end)*100.0/ count(*) desc) as risk_rank
from stg_Churn
group by state

