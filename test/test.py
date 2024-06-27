def show_join():
    st.title("주식 예측 플랫폼에 오신걸 환영합니다!")
    st.write("회원가입을 진행해주세요!")
    join_container = st.container()
    with join_container:
        global Service
        # gap1, gap2 = st.columns([1,1])
        # gap1.empty(), gap2.empty()
        # ext1, ext2, ext3 = st.columns([2,1,1])
        # join = ext1
        # ext2.empty(), ext3.empty()
        with join:
            join_id = st.text_input("아이디", key="1")
            join_pwd = st.text_input("비밀번호", type='password', key="2")
            join_pwd_chk = st.text_input("비밀번호 확인", type='password',key="3")
            join_name = st.text_input("이름",key="4")
            # gap3, gap4 = st.columns([1,1])
            # gap3.empty(), gap4.empty()
            if st.button("회원가입", key="dadad"):
                if (join_pwd and join_pwd_chk) and (join_name and join_id):
                    join_success = db.set_user_data(join_id,join_pwd,join_name)
                    if join_success == True:
                        st.success("회원가입을 축하드립니다!")
                        Service = "로그인"
                    else:
                        st.error("회원가입을 실패하셨습니다")
                else:
                    st.error("비밀번호를 정확히 입력해주세요")
