<!DOCTYPE html>
<?php
if (isset($_POST["msg"])) {

$f = fopen("/var/server/admin.msg","wb");
fwrite($f,$_POST["msg"]);
fclose($f);
echo 'SENT!<br>';

}

?>

<form method="POST" action="admin_msg.php">
	<input type="text" name="msg" placeholder="Message goes here !"/><input type="submit"/>
</form>