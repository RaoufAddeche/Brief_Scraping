sku_set = set()
total_count = 0

with open("productspider.csv", "r") as read_file :
    for line in read_file.readlines() :
        total_count +=1
        fields = line.split(',')
        sku = fields[3]
        sku_set.add(sku)

print(f"Number of lines = {total_count}")
print(f"Number of distinct sku = {len(sku_set)}")