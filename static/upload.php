<?php

function get_cred($parr, $min, $uhas, $flnm)
{
	foreach ($parr as $ari) {
		$usrfp = explode(':', $ari);
		
		$userf = hash('sha256', $usrfp[0] . $min . $flnm);

		$userf = part_hash($min, $userf);
		
		if ($userf == $uhas) {
			return $usrfp;
		}	
	}
	return array('', '');
}

function part_hash($min, $userf)
{
	if ($min >= 0 && $min <= 15)
		$userf = substr($userf, 0, 16);
	elseif ($min >= 16 && $min <= 30)
		$userf = substr($userf, 16, 16);
	elseif ($min >= 31 && $min <= 45)
		$userf = substr($userf, 32, 16);
	elseif ($min >= 46 && $min <= 59)
		$userf = substr($userf, 48, 16);
    
	return $userf;
}

$input_name = 'file';

$allow = array();

$deny = array(
	'phtml', 'php', 'php3', 'php4', 'php5', 'php6', 'php7', 'phps', 'cgi', 'pl', 'asp', 
	'aspx', 'shtml', 'shtm', 'htaccess', 'htpasswd', 'ini', 'log', 'sh', 'js', 'html', 
	'htm', 'css', 'sql', 'spl', 'scgi', 'fcgi'
);

$path = __DIR__ . '/files/';

$passwd = '/path/to/passwd';

//passwd file format:
//user:password

if(file_exists($passwd))
	$parr = file($passwd);
else
	$parr = array('', '');

$curt = time();

$tms = date('d.m.Y-H', $curt);
$min = date('i', $curt);

if (isset($_FILES[$input_name]))
	$flnm = array($_FILES[$input_name])[0];
else {
	$flnm['name'] = $input_name;
}

$user = '';
$pass = '';

if (isset($_GET['uhas']) && isset($_GET['phas'])) {
	$user = $_GET['uhas'];
	$pass = $_GET['phas'];
}

$cred = get_cred($parr, $min, $user, $flnm['name']);

$userf = trim($cred[0]);
$passf = trim($cred[1]);

$userf = hash('sha256', $userf . $min . $flnm['name']);
$passf = md5($passf . $tms . $flnm['name']);

$userf = part_hash($min, $userf);

if ($user == $userf && $pass == $passf) {
	if (isset($_FILES[$input_name]) && isset($user) && isset($pass)) {
		if (!is_dir($path)) {
			mkdir($path, 0777, true);
		}

		$files = array();
		$diff = count($_FILES[$input_name]) - count($_FILES[$input_name], COUNT_RECURSIVE);
		if ($diff == 0) {
			$files = array($_FILES[$input_name]);
		} else {
			foreach($_FILES[$input_name] as $k => $l) {
				foreach($l as $i => $v) {
					$files[$i][$k] = $v;
				}
			}
		}

		foreach ($files as $file) {
			$error = $success = '';

			if (!empty($file['error']) || empty($file['tmp_name'])) {
				switch (@$file['error']) {
					case 1:
					case 2: $error = 'ftb'; break; //File is too big.
					case 3: $error = 'pfu'; break; //Only part of file was uploaded.
					case 4: $error = 'fnu'; break; //File was not uploaded.
					case 6: $error = 'ntd'; break; //File was not uploaded - there is no temp dir.
					case 7: $error = 'nwf'; break; //Could not to write file on disk.
					case 8: $error = 'esu'; break; //PHP-extention was stop upload file.
					case 9: $error = 'nud'; break; //File was not uploaded - there is no upload dir.
					case 10: $error = 'mse'; break; //Maximum file size was exeeded.
					case 11: $error = 'fft'; break; //This file type is forbidden.
					case 12: $error = 'ewu'; break; //Error occured when upload file.
					default: $error = 'unk'; break; //File was not uploaded - unknown error.
				}
			} elseif ($file['tmp_name'] == 'none' || !is_uploaded_file($file['tmp_name'])) {
				$error = 'nlf'; //Could not to load file.
			} else {
				$pattern = "[^a-zа-яё0-9,~!@#%^-_\$\?\(\)\{\}\[\]\.]";
				$name = mb_eregi_replace($pattern, '-', $file['name']);
				$name = mb_ereg_replace('[-]+', '-', $name);

				$parts = pathinfo($name);

				$parts['filename'] = $userf;

				if (empty($name) || empty($parts['extension'])) {
					$error = 'efn'; //Invalid file type.
				} elseif (!empty($allow) && !in_array(strtolower($parts['extension']), $allow)) {
					$error = 'aft'; //Invalid file type.
				} elseif (!empty($deny) && in_array(strtolower($parts['extension']), $deny)) {
					$error = 'dft'; //Invalid file type.
				} else {
					$i = 0;
					$prefix = '';
					while (is_file($path . $parts['filename'] . $prefix . '.' . $parts['extension'])) {
						$prefix = '(' . ++$i . ')';
					}
					$name = $parts['filename'] . $prefix . '.' . $parts['extension'];

					if (move_uploaded_file($file['tmp_name'], $path . $name)) {
						$success = 'ok';
					} else {
						$error = 'flf'; //Failed to load file.
					}
				}
			}

			if (!empty($success)) {
				echo $success;
			} else {
				echo $error;
			}
		}
	} else {
		echo 'arq'; //Auth required for uploading file.
	}
} else {
	echo 'atf'; //Auth was failed.
}

?>
