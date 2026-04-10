def record(acno,t_type,amount,remark,cur,name="Self",mobile="N/A"):
    try:
        query="insert into Transactions(acno,t_type,amount,remark, depositer_name ,depositer_phone) values(%s,%s,%s,%s,%s,%s)"
        value=(acno,t_type,amount,remark,name,mobile)
        cur.execute(query,value)
        last_id=cur.lastrowid
        return last_id
    except Exception as e:
        print("Error",e)