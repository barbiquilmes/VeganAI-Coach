"""
Seed the database with initial recipes.
Run: python -m app.seed_recipes
"""
from app.database import SessionLocal
from app.db_models import Recipe

# Sample vegan recipes
RECIPES = [
    # Indian Curries (7 recipes)
    {
        "title": "Vegan Chickpea Curry (Chana Masala)",
        "ingredients": "2 cups chickpeas (cooked), 1 large onion, 3 tomatoes, 2 tbsp ginger-garlic paste, 1 tsp turmeric, 2 tsp garam masala, 1 tsp cumin seeds, 1 tsp coriander powder, 2 tbsp oil, salt, fresh cilantro",
        "instructions": "Heat oil in a pan. Add cumin seeds. Sauté onions until golden. Add ginger-garlic paste and cook for 2 minutes. Add tomatoes and spices. Cook until tomatoes break down. Add chickpeas and 1 cup water. Simmer for 15 minutes. Garnish with cilantro.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Indian", "difficulty": "Easy", "prep_time": "15 min", "cook_time": "20 min"}
    },
    {
        "title": "Vegan Palak Tofu (Spinach Curry with Tofu)",
        "ingredients": "1 block firm tofu, 2 bunches spinach, 1 onion, 2 tomatoes, 2 green chilies, 1 tbsp ginger, 1 tsp cumin, 1 tsp turmeric, 1 tsp garam masala, 2 tbsp oil, salt",
        "instructions": "Blanch and puree spinach. Pan-fry tofu cubes until golden. In a pan, sauté onions, add tomatoes and spices. Add spinach puree and cook for 10 minutes. Add tofu and simmer for 5 minutes. Serve hot.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Indian", "difficulty": "Medium", "prep_time": "20 min", "cook_time": "25 min"}
    },
    {
        "title": "Vegan Dal Makhani (Creamy Lentil Curry)",
        "ingredients": "1 cup black lentils (urad dal), 1/4 cup kidney beans, 1 onion, 2 tomatoes, 2 tbsp cashew cream, 1 tsp cumin, 1 tsp garam masala, 1 tsp red chili powder, 2 tbsp oil, salt, fresh cream (vegan)",
        "instructions": "Soak lentils and beans overnight. Pressure cook until soft. In a pan, sauté onions, add tomatoes and spices. Add cooked lentils and beans. Simmer for 20 minutes. Add cashew cream. Cook for 10 more minutes. Garnish with vegan cream.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Indian", "difficulty": "Medium", "prep_time": "Overnight soak", "cook_time": "45 min"}
    },
    {
        "title": "Vegan Aloo Gobi (Potato and Cauliflower Curry)",
        "ingredients": "2 potatoes, 1 small cauliflower, 1 onion, 2 tomatoes, 1 tsp turmeric, 1 tsp cumin, 1 tsp coriander powder, 1/2 tsp red chili, 2 tbsp oil, salt, fresh cilantro",
        "instructions": "Cut potatoes and cauliflower into florets. Heat oil, add cumin seeds. Sauté onions until translucent. Add tomatoes and spices. Add vegetables and 1/2 cup water. Cover and cook until tender. Garnish with cilantro.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Indian", "difficulty": "Easy", "prep_time": "15 min", "cook_time": "20 min"}
    },
    {
        "title": "Vegan Baingan Bharta (Roasted Eggplant Curry)",
        "ingredients": "2 large eggplants, 1 onion, 2 tomatoes, 2 green chilies, 1 tbsp ginger, 1 tsp cumin, 1 tsp turmeric, 1 tsp garam masala, 2 tbsp oil, salt, fresh cilantro",
        "instructions": "Roast eggplants over flame or in oven until charred. Peel and mash. Heat oil, sauté onions until golden. Add tomatoes, green chilies, and spices. Cook until tomatoes break down. Add mashed eggplant. Cook for 10 minutes. Garnish with cilantro.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Indian", "difficulty": "Medium", "prep_time": "20 min", "cook_time": "30 min"}
    },
    {
        "title": "Vegan Vegetable Korma",
        "ingredients": "Mixed vegetables (carrots, peas, potatoes, cauliflower), 1 onion, 2 tbsp cashews, 1/2 cup coconut milk, 1 tsp turmeric, 1 tsp garam masala, 1 tsp coriander powder, 2 tbsp oil, salt",
        "instructions": "Soak cashews and blend into paste. Heat oil, sauté onions. Add vegetables and spices. Cook for 5 minutes. Add cashew paste and coconut milk. Simmer until vegetables are tender. Serve with rice or naan.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Indian", "difficulty": "Medium", "prep_time": "15 min", "cook_time": "25 min"}
    },
    {
        "title": "Vegan Rajma Curry (Kidney Bean Curry)",
        "ingredients": "2 cups kidney beans (cooked), 1 onion, 2 tomatoes, 2 tbsp ginger-garlic paste, 1 tsp cumin, 1 tsp coriander powder, 1 tsp garam masala, 1/2 tsp red chili, 2 tbsp oil, salt",
        "instructions": "Heat oil, add cumin seeds. Sauté onions until golden. Add ginger-garlic paste. Add tomatoes and spices. Cook until tomatoes break down. Add kidney beans and 1 cup water. Simmer for 20 minutes. Mash some beans for thickness.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Indian", "difficulty": "Easy", "prep_time": "10 min", "cook_time": "25 min"}
    },
    
    # Thai Recipes (7 recipes)
    {
        "title": "Vegan Pad Thai",
        "ingredients": "200g rice noodles, 200g firm tofu, 2 cups bean sprouts, 3 spring onions, 2 cloves garlic, 3 tbsp tamarind paste, 2 tbsp soy sauce, 1 tbsp brown sugar, 2 tbsp oil, lime, crushed peanuts",
        "instructions": "Soak rice noodles. Pan-fry tofu until crispy. Heat oil, sauté garlic. Add noodles and sauce (tamarind, soy, sugar). Toss well. Add bean sprouts and spring onions. Serve with lime and crushed peanuts.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Thai", "difficulty": "Medium", "prep_time": "15 min", "cook_time": "15 min"}
    },
    {
        "title": "Vegan Green Curry",
        "ingredients": "2 tbsp green curry paste, 1 can coconut milk, 1 block firm tofu, 1 eggplant, 1 bell pepper, 2 kaffir lime leaves, 1 tbsp soy sauce, 1 tsp sugar, Thai basil",
        "instructions": "Cut tofu and vegetables into chunks. Heat 1/4 cup coconut milk, add curry paste. Fry until fragrant. Add remaining coconut milk. Add vegetables and tofu. Simmer for 10 minutes. Add soy sauce and sugar. Garnish with basil.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Thai", "difficulty": "Easy", "prep_time": "10 min", "cook_time": "15 min"}
    },
    {
        "title": "Vegan Tom Yum Soup",
        "ingredients": "4 cups vegetable broth, 2 stalks lemongrass, 3 kaffir lime leaves, 3 slices galangal, 2 red chilies, 200g mushrooms, 1 tomato, 2 tbsp lime juice, 1 tbsp soy sauce, cilantro",
        "instructions": "Bruise lemongrass and cut into pieces. Bring broth to boil. Add lemongrass, lime leaves, and galangal. Simmer for 5 minutes. Add mushrooms and tomato. Cook for 5 minutes. Add lime juice and soy sauce. Garnish with cilantro.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Thai", "difficulty": "Easy", "prep_time": "10 min", "cook_time": "15 min"}
    },
    {
        "title": "Vegan Massaman Curry",
        "ingredients": "2 tbsp massaman curry paste, 1 can coconut milk, 2 potatoes, 1 onion, 1/2 cup peanuts, 1 block tofu, 2 tbsp tamarind paste, 1 tbsp brown sugar, 2 tbsp oil",
        "instructions": "Cut potatoes and tofu into chunks. Heat oil, fry curry paste until fragrant. Add coconut milk. Add potatoes and cook for 10 minutes. Add tofu, peanuts, and onion. Simmer for 15 minutes. Add tamarind and sugar. Serve with rice.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Thai", "difficulty": "Medium", "prep_time": "15 min", "cook_time": "30 min"}
    },
    {
        "title": "Vegan Red Curry with Vegetables",
        "ingredients": "2 tbsp red curry paste, 1 can coconut milk, mixed vegetables (bell peppers, carrots, broccoli), 1 block tofu, 2 kaffir lime leaves, 1 tbsp soy sauce, Thai basil",
        "instructions": "Cut vegetables and tofu. Heat 1/4 cup coconut milk, add curry paste. Fry until fragrant. Add remaining coconut milk. Add vegetables and tofu. Simmer for 12 minutes. Add soy sauce. Garnish with basil.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Thai", "difficulty": "Easy", "prep_time": "10 min", "cook_time": "15 min"}
    },
    {
        "title": "Vegan Pad Krapow (Thai Basil Stir Fry)",
        "ingredients": "200g firm tofu, 2 cups Thai basil, 3 cloves garlic, 2 red chilies, 2 tbsp soy sauce, 1 tbsp dark soy sauce, 1 tsp sugar, 2 tbsp oil, jasmine rice",
        "instructions": "Crumble tofu. Heat oil, fry garlic and chilies. Add tofu and stir-fry until golden. Add soy sauces and sugar. Add basil leaves. Toss quickly. Serve over jasmine rice with fried egg (vegan alternative).",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Thai", "difficulty": "Easy", "prep_time": "5 min", "cook_time": "10 min"}
    },
    {
        "title": "Vegan Thai Yellow Curry",
        "ingredients": "2 tbsp yellow curry paste, 1 can coconut milk, 2 potatoes, 1 onion, 1 block tofu, 1/2 cup coconut cream, 1 tbsp soy sauce, 1 tsp turmeric, 2 tbsp oil",
        "instructions": "Cut vegetables and tofu. Heat oil, fry curry paste. Add coconut milk. Add potatoes and cook for 10 minutes. Add tofu and onion. Simmer for 15 minutes. Add coconut cream and soy sauce. Serve with rice.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Thai", "difficulty": "Easy", "prep_time": "10 min", "cook_time": "25 min"}
    },
    
    # Japanese Recipes (6 recipes)
    {
        "title": "Vegan Miso Soup",
        "ingredients": "4 cups dashi (kombu seaweed broth), 3 tbsp white miso paste, 200g silken tofu, 2 sheets nori, 2 spring onions, wakame seaweed",
        "instructions": "Make dashi by simmering kombu. Remove kombu. Cut tofu into cubes. Soak wakame. Heat dashi, add wakame and tofu. Simmer for 2 minutes. Remove from heat, whisk in miso paste. Add nori strips and spring onions.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Japanese", "difficulty": "Easy", "prep_time": "5 min", "cook_time": "10 min"}
    },
    {
        "title": "Vegan Teriyaki Tofu",
        "ingredients": "1 block firm tofu, 3 tbsp soy sauce, 2 tbsp mirin, 1 tbsp sake, 1 tbsp brown sugar, 1 tsp ginger, 2 tbsp oil, sesame seeds",
        "instructions": "Press tofu and cut into slices. Pan-fry until golden on both sides. Mix soy sauce, mirin, sake, sugar, and ginger. Add sauce to pan. Simmer until thick and glossy. Garnish with sesame seeds.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Japanese", "difficulty": "Easy", "prep_time": "10 min", "cook_time": "15 min"}
    },
    {
        "title": "Vegan Ramen",
        "ingredients": "4 cups vegetable broth, 200g ramen noodles, 1 block marinated tofu, 2 sheets nori, 2 spring onions, 100g shiitake mushrooms, 1 sheet kombu, soy sauce, sesame oil",
        "instructions": "Make broth with kombu and shiitake. Simmer for 20 minutes. Strain. Cook noodles separately. Pan-fry tofu. Heat broth, add soy sauce. Assemble: noodles in bowl, add broth, top with tofu, mushrooms, nori, and spring onions.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Japanese", "difficulty": "Medium", "prep_time": "15 min", "cook_time": "25 min"}
    },
    {
        "title": "Vegan Vegetable Tempura",
        "ingredients": "Mixed vegetables (sweet potato, bell pepper, broccoli, mushrooms), 1 cup all-purpose flour, 1 cup ice-cold sparkling water, 1 tsp baking powder, oil for frying, tempura dipping sauce",
        "instructions": "Cut vegetables into bite-sized pieces. Mix flour, baking powder, and ice-cold water (don't overmix). Heat oil to 180°C. Dip vegetables in batter. Fry until golden and crispy. Serve with tempura dipping sauce.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Japanese", "difficulty": "Medium", "prep_time": "15 min", "cook_time": "15 min"}
    },
    {
        "title": "Vegan Katsu Curry",
        "ingredients": "1 block firm tofu, 2 tbsp curry roux, 1 onion, 1 carrot, 1 potato, 2 cups vegetable broth, panko breadcrumbs, flour, oil for frying, rice",
        "instructions": "Press and cut tofu. Bread with flour, then panko. Deep fry until golden. Sauté onion, carrot, and potato. Add broth and curry roux. Simmer until vegetables are tender. Serve curry over rice with katsu on top.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Japanese", "difficulty": "Medium", "prep_time": "20 min", "cook_time": "25 min"}
    },
    {
        "title": "Vegan Onigiri (Rice Balls)",
        "ingredients": "2 cups cooked sushi rice, 1 sheet nori, 2 tbsp umeboshi (pickled plum) paste, 1/4 cup cooked vegetables, salt, sesame seeds",
        "instructions": "Wet hands with salt water. Take a handful of rice. Make a small indentation. Add filling (umeboshi or vegetables). Shape into triangle. Wrap with nori strip. Repeat. Can add sesame seeds for flavor.",
        "created_by_ai": False,
        "metadata_json": {"cuisine": "Japanese", "difficulty": "Easy", "prep_time": "10 min", "cook_time": "0 min"}
    },
]


def seed_recipes():
    """Add recipes to the database"""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding recipes into database...")
        
        # Check if recipes already exist
        existing_count = db.query(Recipe).count()
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} recipes.")
            response = input("Do you want to add more recipes? (y/n): ")
            if response.lower() != 'y':
                print("❌ Seeding cancelled.")
                return
        
        added = 0
        for recipe_data in RECIPES:
            # Check if recipe with same title exists
            existing = db.query(Recipe).filter(Recipe.title == recipe_data["title"]).first()
            if existing:
                print(f"⏭️  Skipping '{recipe_data['title']}' (already exists)")
                continue
            
            recipe = Recipe(**recipe_data)
            db.add(recipe)
            added += 1
            print(f"✅ Added: {recipe_data['title']}")
        
        db.commit()
        print(f"\n🎉 Successfully added {added} new recipes!")
        print(f"📊 Total recipes in database: {db.query(Recipe).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding recipes: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_recipes()

