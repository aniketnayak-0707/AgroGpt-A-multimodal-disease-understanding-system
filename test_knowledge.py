from core.knowledge import get_disease_info

print("\nFirst call (should NOT use cache):\n")
info1 = get_disease_info("tomato___late_blight")
print(info1)

print("\nSecond call (should USE cache):\n")
info2 = get_disease_info("tomato___late_blight")
print(info2)