# Open the file in write mode
with open("8_CS.txt", "w") as f:
    f.write("""*VERSION 3DEXPERIENCER2022x
*NULL $
*SEPARATOR ;
""")
    for i in range(101):
        # Format the number as a 3-digit string (e.g., 0 becomes '000')
        num = f"{i:03d}"
        
        # Write the two required lines
        f.write(f"*PROJECT CS_{num};$;CS_{num};Team;DesignTeam\n")
        f.write("+VISIBILITY Public\n")