/*
  �����:                __author__
  ����:                 %date%
  ����� �����:          %ver%
  ����� ������:         __ticket_num__
  ����� �������:        __new_objs__
  ���������� �������:   __modify_objs__
  ��������� �������:    __del_objs__
  �����������:     	__comment_body__
  
    ������: %timestamp%
    ������ ���������� ������: %changed%


*/


__list_objs__
/


-- ������������� ��� ���������� �������
begin
  dbms_utility.compile_schema(schema => user, compile_all => false, reuse_settings => true);
end;
/

update FW_VERSION_PROJECT set N_DATABASE_VER = %ver% where V_PROJECT = '__project__';
commit
/
