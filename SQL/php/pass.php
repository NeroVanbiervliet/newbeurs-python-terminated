<?php
$password = "louis";

$hashed = password_hash($password, PASSWORD_DEFAULT);

$succeeded = password_verify($password, $hashed);

if($succeeded)
{
	echo("ok");
}
else
{
	echo("niet ok");
}	

?>
