<?php
$servername = "localhost";
$username = "root";
$password = "lnrddvnc";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully";

$conn->select_db("oakTest");

// Query
$query = "SHOW TABLES";
//$query = "CREATE DATABASE oakTest";



$result = $conn->query($query);


$converted_res = ($result) ? 'true' : 'false';
echo($converted_res);

while($row = $result->fetch_assoc()){
    print_r($row);
}
?>
