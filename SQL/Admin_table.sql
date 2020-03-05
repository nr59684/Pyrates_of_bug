CREATE table Admin
(
	AdminID int auto_increment key,
    AdminName varchar(200),
    AdminPassword varchar(100),
    AdminEmail varchar(200),
    AdminPhoto varchar(500)
)
Insert into Admin(AdminName,AdminPassword,AdminEmail,AdminPhoto)
values('Nilesh','groot','rijhwaninilesh@gmail.com','nilesh1.jpg')
