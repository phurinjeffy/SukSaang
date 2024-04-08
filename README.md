# SukSaang

Our food ordering system provides a convenient and efficient way for customers to order their favorite meals. 
The system streamlines the ordering process for both customers and restaurants.

Developed using PyScript for front-end framework, FastAPI for back-end, and ZODB as object-oriented database.

<br>

## Screen Captures

***User Side***
- **Menu** - displays the categories and menu items
  
<img width="1512" alt="image" src="https://github.com/phurinjeffy/SukSaang/assets/110296454/87373fc2-92fd-4845-a363-98e4b147ede1">
<br>
<br>

- **Cart** - keep track of what the user's has put into the cart
<img width="1512" alt="image" src="https://github.com/phurinjeffy/SukSaang/assets/110296454/ecaacc02-5773-4264-bc38-a6b59fa72b8f">
<br>
<br>

***Admin Side***
- **Statistics** - displays the shop statistics and sales for each month
  
<img width="1512" alt="image" src="https://github.com/phurinjeffy/SukSaang/assets/110296454/476c4706-00ec-4515-8d6f-e5d4dc67855c">
<br>
<br>

- **Adjust Menu** - allow admins to create, update, delete the menu items
<img width="1512" alt="image" src="https://github.com/phurinjeffy/SukSaang/assets/110296454/21b6a883-adcb-41a7-a272-48e70a7981d6">
<br>
<br>


## How to run

In the server directory, run `python3 main.py`,

Navgiate to the client directory, then run `npm run dev` or `yarn dev`.

Note that an .env file, with the following variables, is needed:
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- S3_BUCKET_NAME
