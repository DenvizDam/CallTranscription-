


p = enhance_prompt(text)
print(p[p.find("<hints>"):p.find("</hints>")+8])


print(p[p.find("<pattern>"):p.find("</pattern>")+10])
