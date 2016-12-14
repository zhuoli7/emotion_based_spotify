<?php
//$picture = "/var/www/html/face.jpg";
//echo $picture;
$result = exec("python /var/www/html/face.py");
$qwe = "Your emotion is: ";
echo $qwe;
//echo $result;

require_once('../mysqli_connection.php');
$query = "SELECT $result FROM music";
$response = @mysqli_query($dbc, $query);
if($response){
$emptyarray=array();
while($row = mysqli_fetch_assoc($response)){
    $emptyarray[]= $row;
}
echo json_encode($emptyarray,JSON_UNESCAPED_SLASHES);
} else {
echo "Couldn't issue database query<br />";
echo mysqli_error($dbc);
}
mysqli_close($dbc);


?>
