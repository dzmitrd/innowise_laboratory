# Define a Function for the Profile & Calculations
def generate_profile(age):
    if 0 <= age <= 12:
        return 'Child'
    elif 12 < age <= 19:
        return 'Teenager'
    else:
        return 'Adult'


# Get User Input
user_name = input("Enter your full name: ").strip()
birth_year_str = input("Enter your birth year: ").strip()
birth_year = int(birth_year_str)
current_age = 2025 - birth_year
hobbies = []
while True:
    tmp_hobby = input("Enter your favorite hobby or type 'stop' to finish: ").strip().capitalize()
    if tmp_hobby.lower() == 'stop':
        break
    else:
        hobbies.append(tmp_hobby)

# Process and Generate the Profile
life_stage = generate_profile(current_age)

user_profile = dict()
user_profile['Name'] = user_name
user_profile['Age'] = current_age
user_profile['Life Stage'] = life_stage
user_profile['Hobbies'] = hobbies

# Display the Output
print(f'Profile Summary:',
      f'Name: {user_profile["Name"]}',
      f'Age: {user_profile["Age"]}',
      f'Life Stage: {user_profile["Life Stage"]}',
      sep='\n')

if hobbies:
    print(f'Favorite Hobbies ({len(hobbies)}):')
    for i in hobbies:
        print('-', i)
else:
    print("You didn't mention any hobbies.")
