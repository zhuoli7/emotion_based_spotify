<?php
$result = exec("python face1.py");
$result_array = json_decode($result);
foreach ($result_array as $row){
    echo $row,"<BR>";
}
?>
