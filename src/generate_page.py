import os
from markdown_blocks import markdown_to_html_node
from extract_markdown import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using '{template_path}'")
    
    with open(from_path, mode='r') as markdown_file:
        markdown_content = markdown_file.read()
    with open(template_path, mode='r') as template_file:
        template_content = template_file.read()
    title = extract_title(markdown_content)
    html_node = markdown_to_html_node(markdown_content)
    markdown_html = html_node.to_html()
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", markdown_html).replace('href="/', f'href="{basepath}/').replace('src="/', f'src="{basepath}/')
    directory = os.path.dirname(dest_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(full_html)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Generating pages recursively from {dir_path_content} to {dest_dir_path} using '{template_path}'")
    
    items = os.listdir(dir_path_content)
    for item in items:
        source_item = os.path.join(dir_path_content, item)
        dest_item = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(source_item):
            if source_item.endswith('.md'):
                generate_page(
                    from_path=source_item,
                    template_path=template_path,
                    dest_path=dest_item.replace('.md', '.html'),
                    basepath=basepath
                )
        else:
            generate_pages_recursive(source_item, template_path, dest_item, basepath)