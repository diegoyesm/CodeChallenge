
<?php

header('Content-Type: text/html; charset=utf-8');
require "Mail.php";
require ('conexion_db.php');

//inicio del envio al correo
$audiencia = mysql_query("
select 
$id, $email, $name, $lastname
from table u
where ...
group by ...

//echo "BEGIN" ;

	while($row=  mysql_fetch_array($QUERY))
     {

	sendEmail($row[0],$row[1],$row[2],$row[3]);
	// envioCorreos($row[0],$row[1]);

      }


function sendEmail($id, $email, $name, $lastname){


   // Include the Mail package

   // Identify the sender, recipient, mail subject, and body
   $sender    = "estadistica@funcionjudicial.gob.ec";



   $recipient = $email; 
   $subject   = "...";
   $body  = "
	      "; 

   // Identify the mail server, username, password, and port  "X.X.X.X"; "mail.XX.XX";

   $server   = "mail.XX.XX";
   $port     = "25";


   // Set up the mail headers
   $headers = array(
      "From"    => $sender,
      "To"      => $recipient,
      "Subject" => $subject
//	  ,"Headers" => $headers
	
   );

   // Configure the mailer mechanism
   $smtp = Mail::factory("smtp",
      array(
        "host"     => $server,
        "port"     => $port,
        "auth"     => FALSE,
        "debug"     => FALSE
      )
   );


   // Send the message
   $mail = $smtp->send($recipient, $headers, $body);


   if (PEAR::isError($mail)) {
      echo ($mail->getMessage());
   } 
   else {
//	echo("<p>Email sent sucesfully.</p>");
	
	$insrus1= mysql_query ("INSERT INTO `LOG_EMAIL` ( ($id, $email, $name, $lastname, '$subject', '$body' )");

   }

//echo "END";


}

?>
