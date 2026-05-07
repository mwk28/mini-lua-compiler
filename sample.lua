--[[
  Mini Compiler Sample Script
  Demonstrating all restricted Lua-like features
]]

-- Variable Declarations and Arithmetic
a = 10
b = 20
c = a + b * 2 -- Multiplication precedence
d = 2 + 3 * 4 -- Constant folding opportunity (should fold to 14)

-- If Else Control Flow
if a < b then
    max_val = b
else
    max_val = a
end

-- While Loop
count = 0
while count < 5 do
    count = count + 1
end

-- For Loop
sum = 0
for i = 1, 10 do
    sum = sum + i
end

-- Function Definition
function calculate_area(width, height)
    area = width * height
    return area
end

-- Function Call (TAC handles definitions, semantic tracks them)
result = 100
return result
