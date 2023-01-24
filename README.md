# Transport App Django
Backend service for project in Database classes.

Procedure:
```
create or replace procedure changeKilometersDone(vehicleVIN string, newKilometersDone dec)
language plpgsql
as $$
begin
    update exampleapp_vehicle set kilometers_done = newKilometersDone where vin=vehicleVIN;
end;
$$;
```

Function:
```
CREATE OR REPLACE FUNCTION sum_income()
  RETURNS double AS $total$ 
declare 
    total double;
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
    SELECT sum(amount) into total FROM exampleapp_invoices;
       RETURN total;
END;
$$
```
