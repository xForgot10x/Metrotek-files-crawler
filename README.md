# Metrotek-files-crawler
Simple crawler made for parsing FTP-like folder structures, used for Metrotek's website in this case.

I was looking for a piece of software for working with files obtained from Metrotek devices, but could not find it anywhere. In the end I ran into http://ntc.metrotek.ru/files/ which is basically an FTP-server-like structure of files and folders. Rather than going through those folders manually, I decided to make a basic crawler to retrieve all of the available links, so that I could filter for file names using DB Browser.

I figured the website would have no crawling protection, so the only constraint I employed is one second delay after every URL request, just in case.

Search for that software was a necessity at work, but since this script contains no confidential data, and most of its code can be reused, I am publishing it here.
