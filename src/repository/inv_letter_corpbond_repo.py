from mysql.connector import connect

def fetch_data(conn: connect):
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT 
        oh.acct_desc, 
        oh.invs_ktp_num, 
        oh.invs_npw_num, 
        oh.invs_passport_num, 
        oh.addr1, 
        oh.addr2,
        oh.addr3,
        oh.rec_bal, 
        oh.rec_dt, 
        oh.eff_dt, 
        oh.client_code,
        oi.sec_code, 
        oi.sec_nm, 
        oi.code_base_cur, 
        oi.mem_nm,
        oi.mem_code,
        oi.trustee, 
        oi.ca_desc, 
        oi.next_day
    FROM ktur_report kr
    JOIN obligasi_holder oh ON kr.id_holder = oh.id_holder
    JOIN obligasi_info oi ON kr.id_info = oi.id_info
    """
    try:
        cursor.execute(query)
        results = cursor.fetchall()

        result_dict = {"data": results}
        
        return result_dict
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
