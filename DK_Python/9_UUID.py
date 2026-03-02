import uuid

# Generate a random UUID (version 4)
unique_id = uuid.uuid4()

print(f"UUID: {unique_id}")
# If you need it as a simple string:
print(f"String format: {str(unique_id)}")