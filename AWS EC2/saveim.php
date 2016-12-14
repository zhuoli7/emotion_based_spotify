<?php
move_uploaded_file($_FILES['webcam']['tmp_name'], 'face.jpg');
$target_dir = "/var/www/html";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name.jpeg"]);
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["name.jpeg"]);
    if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}
?>
