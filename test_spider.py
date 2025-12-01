from baidu_spider import BaiduSpider

def test_spider():
    """
    测试百度爬虫功能，验证是否正确提取标题、摘要、URL和封面URL
    """
    print("开始测试百度爬虫...")
    
    # 创建爬虫实例
    spider = BaiduSpider()
    
    # 使用固定关键词测试搜索功能
    test_keyword = "成都"
    print(f"测试搜索关键词: {test_keyword}")
    
    # 执行搜索
    html_content = spider.search(test_keyword)
    
    if html_content:
        print("✓ 搜索请求成功")
        print(f"返回的HTML内容长度: {len(html_content)} 字符")
        
        # 保存HTML用于调试
        with open('debug_html.txt', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("HTML内容已保存到 debug_html.txt 文件")
        
        # 尝试解析结果
        results = spider.parse_results(html_content)
        
        if results:
            print(f"✓ 解析成功，找到 {len(results)} 条结果")
            
            # 验证字段提取
            field_verification = {
                'title': 0,
                'url': 0,
                'abstract': 0,
                'cover_url': 0
            }
            
            print("\n前3条结果示例:")
            for i, result in enumerate(results[:3], 1):
                print(f"\n第{i}条结果:")
                print(f"标题: {result.get('title', '未提取')}")
                print(f"URL: {result.get('url', result.get('link', '未提取'))}")
                print(f"摘要: {result.get('abstract', '未提取')}")
                print(f"封面URL: {result.get('cover_url', '未提取')}")
                print("-" * 40)
                
                # 更新字段验证计数
                if 'title' in result and result['title']:
                    field_verification['title'] += 1
                if ('url' in result and result['url']) or ('link' in result and result['link']):
                    field_verification['url'] += 1
                if 'abstract' in result and result['abstract']:
                    field_verification['abstract'] += 1
                if 'cover_url' in result and result['cover_url']:
                    field_verification['cover_url'] += 1
            
            # 打印字段提取统计
            print("\n字段提取统计:")
            for field, count in field_verification.items():
                print(f"{field}: 成功提取 {count} 条")
            
            # 保存测试结果
            test_filename = 'test_results.txt'
            spider.save_results(results, test_filename)
            print(f"✓ 结果已保存到 {test_filename}")
        else:
            print("✗ 未能解析到搜索结果（百度可能更新了页面结构）")
    else:
        print("✗ 搜索请求失败")
    
    print("\n测试完成!")


if __name__ == "__main__":
    test_spider()