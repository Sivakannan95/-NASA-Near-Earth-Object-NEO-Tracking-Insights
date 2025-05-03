import streamlit as st
import pandas as pd
import pymysql
import datetime
import base64

# Connect to MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='nasa_pro_1'
)
cur = connection.cursor()

st.set_page_config(layout="wide")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://cdn.i-scmp.com/sites/default/files/styles/1200x800/public/d8/images/canvas/2025/02/10/eb8cfa77-dda4-4cc3-8250-d7577d797f4d_55e3851b.jpg?itok=YtdX9olV&v=1739195162");  /* Example image URL */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center; color: blue'>🚀𝘈𝘴𝘵𝘦𝘳𝘰𝘪𝘥 𝘐𝘯𝘧𝘰𝘳𝘮𝘢𝘵𝘪𝘰𝘯🛰️</h1>",
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(['Asteroid filter', 'Frequently Asked Questions'])

with tab1:
    st.markdown(
        "<h2 style='text-align: center; color: red'>🚀Find Asteroid🔎💫</h2>",
        unsafe_allow_html=True
    )

    spacer1, col1, spacer2, col2, spacer3, col3 = st.columns([0.5, 2, 0.5, 2, 0.5, 2])

    with col1:
        cur.execute("SELECT MIN(absolute_magnitude_h), MAX(absolute_magnitude_h) FROM asteroids;")
        min_mag, max_mag = cur.fetchone()
        smin_mag, smax_mag = st.slider(
            "Absolute Magnitude Range",
            min_value=float(min_mag),
            max_value=float(max_mag),
            value=(float(min_mag), float(max_mag))
        )

        cur.execute("SELECT MIN(estimated_diameter_min_km), MAX(estimated_diameter_min_km) FROM asteroids;")
        min_min_dia, max_min_dia = cur.fetchone()
        smin_min_dia, smax_min_dia = st.slider(
            "Estimated Min Diameter (km)",
            min_value=float(min_min_dia),
            max_value=float(max_min_dia),
            value=(float(min_min_dia), float(max_min_dia))
        )

        cur.execute("SELECT MIN(estimated_diameter_max_km), MAX(estimated_diameter_max_km) FROM asteroids;")
        min_max_dia, max_max_dia = cur.fetchone()
        smin_max_dia, smax_max_dia = st.slider(
            "Estimated Max Diameter (km)",
            min_value=float(min_max_dia),
            max_value=float(max_max_dia),
            value=(float(min_max_dia), float(max_max_dia))
        )

    with col2:
        cur.execute("SELECT MIN(relative_velocity_kmph), MAX(relative_velocity_kmph) FROM close_approach;")
        min_vel, max_vel = cur.fetchone()
        smin_vel, smax_vel = st.slider(
            "Velocity (kmph) Range",
            min_value=float(min_vel),
            max_value=float(max_vel),
            value=(float(min_vel), float(max_vel))
        )

        cur.execute("SELECT MIN(astronomical), MAX(astronomical) FROM close_approach;")
        min_ast, max_ast = cur.fetchone()
        smin_ast, smax_ast = st.slider(
            "Astronomical Range",
            min_value=float(min_ast),
            max_value=float(max_ast),
            value=(float(min_ast), float(max_ast))
        )

        hazard_option = st.selectbox(
            "Asteroid is considered hazardous?",
            options=["Both", "True", "False"]
        )
        

    with col3:
        st.write("📅 Filter by Date Range")
        start_date = st.date_input("Start Date", value=datetime.date(2024, 1, 1))
        end_date = st.date_input("End Date", value=datetime.date(2025, 4, 30))

        if start_date > end_date:
            st.error("Start date must be before end date!")

 
    filter_query = """
        SELECT * FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE a.absolute_magnitude_h BETWEEN %s AND %s
        AND a.estimated_diameter_min_km BETWEEN %s AND %s
        AND a.estimated_diameter_max_km BETWEEN %s AND %s
        AND c.relative_velocity_kmph BETWEEN %s AND %s
        AND c.astronomical BETWEEN %s AND %s
        AND c.close_approach_date BETWEEN %s AND %s
    """

    params = [
        smin_mag, smax_mag,
        smin_min_dia, smax_min_dia,
        smin_max_dia, smax_max_dia,
        smin_vel, smax_vel,
        smin_ast, smax_ast,
        start_date, end_date
    ]

    if hazard_option == "True":
        filter_query += " AND a.is_potentially_hazardous_asteroid = TRUE"
    elif hazard_option == "False":
        filter_query += " AND a.is_potentially_hazardous_asteroid = FALSE"

    filter_query += " ORDER BY c.close_approach_date ASC"
   
    cur.execute(filter_query, params)
    results = cur.fetchall()
    columns = [col[0] for col in cur.description]
    df = pd.DataFrame(results, columns=columns)

    st.write("Filtered Results:")
    st.dataframe(df)

with tab2:

    st.markdown(
        "<h2 style='text-align: center; color: red'>👨‍🚀Questions About Asteroid📝💫</h2>",
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])

with center:

    question = st.selectbox('Questions And Answer About Asteroid',
                          ['1. Count how many times each asteroid has approached Earth',
                           '2. Average velocity of each asteroid over multiple approaches',
                           '3. List top 10 fastest asteroids',
                           '4. Find potentially hazardous asteroids that have approached Earth more than 3 times',
                           '5. Find the month with the most asteroid approaches',
                           '6. Get the asteroid with the fastest ever approach speed',
                           '7. Sort asteroids by maximum estimated diameter (descending)',
                           '8. Asteroids whose closest approach is getting nearer over time',
                           '9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth.',
                           '10. List names of asteroids that approached Earth with velocity > 50,000 km/h',
                           '11. Count how many approaches happened per month',
                           '12. Find asteroid with the highest brightness (lowest magnitude value)',
                           '13. Get number of hazardous vs non-hazardous asteroids',
                           '14. Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance.',
                           '15. Find asteroids that came within 0.05 AU(astronomical distance)',
                           '16. How many asteroid approaches are recorded each day?',
                           '17. Which is the largest asteroid?',
                           '18.Give the asteroid close approach date and before that when it approached',
                           '19. Compare asteroids with the highest and lowest brightness levels',
                           '20. How many unique asteroids have been tracked in total?']
                           )

    if question == '1. Count how many times each asteroid has approached Earth':
        que = '''
        SELECT a.id, a.name, COUNT(a.id) AS count_each_asteroid_approach_earth 
        FROM 
            (SELECT DISTINCT id, name FROM asteroids) a 
        JOIN 
            close_approach c ON a.id = c.neo_reference_id
        GROUP BY 
            a.id, a.name  
        ORDER BY 
            count_each_asteroid_approach_earth DESC
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)

    elif question == '2. Average velocity of each asteroid over multiple approaches':
        que = '''
        select a.id, a.name, round(avg(c.relative_velocity_kmph),2) as Average_Velocity_of_Each_Asteroid from 
        (select distinct id, name from asteroids) a 
        join close_approach c on a.id = c.neo_reference_id
         group by a.id, a.name
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)

    elif question == '3. List top 10 fastest asteroids':
        que = '''
        select * from (select a.id, a.name, c.relative_velocity_kmph as Velocity_kmph, rank() over(order by c.relative_velocity_kmph desc) as Ranks
         from (select distinct id, name from asteroids) a 
        join close_approach c on a.id = c.neo_reference_id) a where Ranks <= 10
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '4. Find potentially hazardous asteroids that have approached Earth more than 3 times':
        que = '''
        select ab.*, b.is_potentially_hazardous_asteroid from (select a.id, a.name, count(a.id) as count_each_asteroid_approach_earth from 
        (select distinct id, name from asteroids) a join close_approach c on a.id = c.neo_reference_id
        group by a.id, a.name) ab join asteroids b on ab.id = b.id where is_potentially_hazardous_asteroid =true and  
        count_each_asteroid_approach_earth > 3 order by count_each_asteroid_approach_earth desc
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)

    elif question == '5. Find the month with the most asteroid approaches':
        que = '''
        select  date_format(close_approach_date,'%M %Y') as Approach_month_And_Year, count(neo_reference_id) as 
        Monthly_count_asteroid_approachs_earth from close_approach group by  date_format(close_approach_date,'%M %Y') 
        order by count(neo_reference_id) desc limit 1
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '6. Get the asteroid with the fastest ever approach speed':
        que = '''
        select a.id, a.name, c.relative_velocity_kmph from (select distinct id, name from asteroids) a 
        join close_approach c on a.id = c.neo_reference_id where c.relative_velocity_kmph = 
        (select max(relative_velocity_kmph) from close_approach)
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '7. Sort asteroids by maximum estimated diameter (descending)':
        que = '''
        select a.id,a.name, a.estimated_diameter_max_km from asteroids a join (select neo_reference_id from close_approach)
        c on a.id = c.neo_reference_id order by a.estimated_diameter_max_km desc
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '8. Asteroids whose closest approach is getting nearer over time':
        que = '''
        select a.id, a.name, c.close_approach_date, c.miss_distance_km from (select distinct id, name from asteroids) a join close_approach c
        on a.id = c.neo_reference_id order by a.id, c.close_approach_date desc
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth.':
        que = '''
        select a.id, a.name, c.close_approach_date, c.miss_distance_km from (select distinct id, name from asteroids) a join close_approach c
        on a.id = c.neo_reference_id order by a.id, miss_distance_km
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '10. List names of asteroids that approached Earth with velocity > 50,000 km/h':
        que = '''
        select a.id, a.name, c.relative_velocity_kmph from (select distinct id, name from asteroids) a join close_approach c
        on a.id = c.neo_reference_id where c.relative_velocity_kmph>50000 order by relative_velocity_kmph
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '11. Count how many approaches happened per month':
        que = '''
        select  date_format(close_approach_date,'%M %Y') as Approach_month_And_Year, count(neo_reference_id) as 
        Monthly_count_asteroid_approachs_earth from close_approach group by  date_format(close_approach_date,'%M %Y') 
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '12. Find asteroid with the highest brightness (lowest magnitude value)':
        que = '''
        select a.id, a.name, a.absolute_magnitude_h from (select distinct neo_reference_id from close_approach) c join asteroids a
        on a.id = c.neo_reference_id order by a.absolute_magnitude_h asc limit 1 
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '13. Get number of hazardous vs non-hazardous asteroids':
        que = '''
        select a.is_potentially_hazardous_asteroid, count(a.is_potentially_hazardous_asteroid) from asteroids a join
        (select distinct neo_reference_id from close_approach) c on a.id = c.neo_reference_id
        group by a.is_potentially_hazardous_asteroid
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '14. Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance.':
        que = '''
        select a.id, a.name, c.close_approach_date, c.miss_distance_km from (select distinct id, name from asteroids) a join close_approach c
        on a.id = c.neo_reference_id where c.miss_distance_km <384400 order by c.miss_distance_km
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '15. Find asteroids that came within 0.05 AU(astronomical distance)':
        que = '''
        select a.id, a.name, c.astronomical from (select distinct id, name from asteroids) a join close_approach c
        on a.id = c.neo_reference_id where astronomical < 0.05 order by c.astronomical
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '16. How many asteroid approaches are recorded each day?':
        que = '''
        select close_approach_date, count(close_approach_date) as count_of_everyday from close_approach 
        group by close_approach_date order by close_approach_date
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '17. Which is the largest asteroid?':
        que = '''
        SELECT * FROM asteroids WHERE estimated_diameter_max_km = (SELECT MAX(estimated_diameter_max_km) FROM asteroids);
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '18.Give the asteroid close approach date and before that when it approached':
        que = '''
        SELECT * FROM (SELECT c.neo_reference_id, a.name, c.close_approach_date,
        LAG(c.close_approach_date) OVER (PARTITION BY c.neo_reference_id ORDER BY c.close_approach_date) AS previous_approach_date 
        FROM close_approach c
        JOIN (select distinct id,name from asteroids) a ON c.neo_reference_id = a.id) sub WHERE previous_approach_date IS NOT NULL;
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '19. Compare asteroids with the highest and lowest brightness levels':
        que = '''
        select id, name, absolute_magnitude_h, case when absolute_magnitude_h> (select avg(absolute_magnitude_h) from asteroids) then 'Brightest asteroid'
 when absolute_magnitude_h < (select avg(absolute_magnitude_h) from asteroids) then 'Dimmest asteroid' else 'Average' end as levels from asteroids
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    elif question == '20. How many unique asteroids have been tracked in total?':
        que = '''
        SELECT COUNT(DISTINCT id) AS total_unique_asteroids FROM asteroids;
        '''
        cur.execute(que)
        ans = cur.fetchall()
        ans_columns = [col[0] for col in cur.description]

        answer = pd.DataFrame(ans, columns=ans_columns)
        st.write("Answer:")
        st.dataframe(answer)
    else:
        st.write('Welcome')







