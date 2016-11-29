<?php
$result = exec("python f_array.py");
$result_array = json_decode($result);
foreach ($result_array as $row){
    echo $row,"<BR>";
}
?>

