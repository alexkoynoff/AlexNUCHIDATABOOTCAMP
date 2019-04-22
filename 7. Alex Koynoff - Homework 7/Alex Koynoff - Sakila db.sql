
-- 1a. Display the first and last names of all actors from the table actor.

select first_name, last_name from actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.

select  upper(concat(first_name,' ', last_name)) as "Actor Name" from actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?

select * from actor where first_name="Joe";

-- 2b. Find all actors whose last name contain the letters GEN.

select * from actor where last_name like "%GEN%";

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order.

select last_name, first_name from actor where last_name like "%LI%" order by last_name, first_name;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China

select country_id, country from country where country in ('Afghanistan', 'Bangladesh', 'China')

-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor 
-- named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).

alter table actor
add column description blob;

select * from actor #to check that the new column was successfuly added

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.

alter table actor
drop column description;

select * from actor #to check that the new column was successfuly removed

-- 4a. List the last names of actors, as well as how many actors have that last name.

select last_name, count(*) as "Count of Last Name" from actor group by last_name;


-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors

select last_name, count(*) as "Count of Last Name 2 or more" from actor group by last_name having count(*)>=2;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.

select actor_id, first_name, last_name from actor where first_name='GROUCHO'; #to see data before change

update actor
set first_name="HARPO"
where actor_id=172;

select first_name, last_name from actor where first_name='GROUCHO'; #to see data after change

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.

select actor_id, first_name, last_name from actor where first_name='HARPO'; #before change

update actor
set first_name="GROUCHO"
where actor_id=172;

select first_name, last_name from actor where first_name='GROUCHO'; #to see data after change

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?

show create table address; 
        #OR the below
show columns from address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address.

select staff.first_name, staff.last_name, address.address
from staff
	inner join address on
	address.address_id=staff.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.

select * from payment

select payment.staff_id,staff.first_name, staff.last_name, sum(payment.amount)
from staff
	inner join payment on
	staff.staff_id=payment.staff_id
	where date(payment.payment_date) between date('2005-08-01') and date('2005-08-31')
	group by payment.staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.

select film.title, count(film_actor.actor_id) as "Count of Actors in Film"
from film
	inner join film_actor on
	film.film_id=film_actor.film_id
	group by film.title

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?

select * from inventory

select film.title, count(inventory.film_id) as "Number of Inventory Copies"
from film
	inner join inventory on
	film.film_id=inventory.film_id
	where title='Hunchback Impossible'

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:

select customer.first_name, customer.last_name, sum(payment.amount)
from customer
	inner join payment on
	customer.customer_id=payment.customer_id
	group by customer.last_name
	order by customer.last_name asc

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. 
-- Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.

-- using subquery
select title
from film
	where language_id 
	in (
		select language_id 
		from language
        where name="English"
)
and title like "K%" or title like "Q%";

#----------------------------------------------------

-- using JOIN
select film.title, film.language_id, language.name
from film
	inner join language on
    film.language_id=language.language_id
    where title like "K%" or title like "Q%";
    
-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.

select actor_id, first_name, last_name
from actor 
where actor_id
in(
	select actor_id
		from film_actor
        where film_id
        in(
			select film_id
            from film
            where title="Alone Trip"
        )
);

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.

Select customer.first_name, customer.last_name, customer.email, country.country
from customer
	inner join address 
	on customer.address_id=address.address_id
		inner join city
        on address.city_id=city.city_id
			inner join country
            on city.country_id=country.country_id
            where country.country="Canada";
            
-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.

select * from category

select film.title, category.name
from film
	inner join film_category
    on film.film_id=film_category.film_id
		inner join category
        on film_category.category_id=category.category_id
        where category.name="Family";
        
        
-- 7e. Display the most frequently rented movies in descending order.

select * from rental

select film.title, count(rental.inventory_id) as "Rental Count"
from film
	inner join inventory
    on film.film_id=inventory.film_id
		inner join rental
        on inventory.inventory_id=rental.inventory_id
        group by film.title
        order by count(rental.inventory_id) desc
        limit 10;          #displays top 10
        
-- 7f. Write a query to display how much business, in dollars, each store brought in.

select customer.store_id, sum(payment.amount) as "Total Sales per Store"
from customer
	inner join payment
    on customer.customer_id=payment.customer_id
    group by customer.store_id;
 

-- 7g. Write a query to display for each store its store ID, city, and country.

select customer.store_id, city.city, country.country
from customer
	inner join address
	on customer.address_id=address.address_id
		inner join city
        on address.city_id=city.city_id
			inner join country
            on city.country_id=country.country_id;

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)

select category.name, sum(payment.amount)
from category
	inner join film_category
	on category.category_id=film_category.category_id
		inner join inventory
        on film_category.film_id=inventory.film_id
			inner join rental
            on inventory.inventory_id=rental.inventory_id
				inner join payment
                on rental.rental_id=payment.rental_id
                group by category.name
                order by sum(payment.amount) desc
                limit 5
                
-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. 
-- If you haven't solved 7h, you can substitute another query to create a view.

create view top_five_genres_by_revenue as
select category.name, sum(payment.amount)
from category
	inner join film_category
	on category.category_id=film_category.category_id
		inner join inventory
        on film_category.film_id=inventory.film_id
			inner join rental
            on inventory.inventory_id=rental.inventory_id
				inner join payment
                on rental.customer_id=payment.customer_id
                group by category.name
                order by category.name desc
                limit 5

show tables       #to show that the view is available
show full tables in sakila where TABLE_TYPE like 'view';    #shows all "view" table types

-- 8b. How would you display the view that you created in 8a?

select * from top_five_genres_by_revenue

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.

drop view if exists top_five_genres_by_revenue

show tables       #to show that the view is not there anymore




