import sys
from utils import read_csv, fetch_external_data

def main(csv_file_path):
    products = read_csv(csv_file_path)
    if not products:
        print("No products to analyze.")
        return
    
    external_data = fetch_external_data('https://api.priceapi.com/v2/jobs')
    if not external_data:
        print("Failed to fetch external data.")
        return
    
    # Generate insights: Compare our prices with market prices and identify stock issues
    insights = []
    if isinstance(external_data, list):
        for product in products:
            market_price = next((item['price'] for item in external_data if item['product_name'] == product['product_name']), None)
            if market_price:
                price_diff = float(product['our_price']) - market_price
                insights.append({
                    'product_name': product['product_name'],
                    'our_price': product['our_price'],
                    'market_price': market_price,
                    'price_difference': price_diff,
                    'current_stock': product['current_stock'],
                    'restock_threshold': product['restock_threshold']
                })
    
    try:
        with open('report.md', 'w') as report_file:
            report_file.write("# Pricing Insights Report\n\n")
            report_file.write("## Summary of Data Cleaning Steps\n")
            report_file.write("- Removed rows with missing prices\n")
            report_file.write("- Standardized category names\n\n")
            report_file.write("## Key Insights Discovered\n")
            for insight in insights:
                report_file.write(f"### {insight['product_name']}\n")
                report_file.write(f"- Our Price: ${insight['our_price']}\n")
                report_file.write(f"- Market Price: ${insight['market_price']}\n")
                report_file.write(f"- Price Difference: ${insight['price_difference']}\n")
                if float(insight['price_difference']) > 5:
                    report_file.write(f"  - Insight: Our price is significantly higher than the market price.\n")
                elif float(insight['price_difference']) < -5:
                    report_file.write(f"  - Insight: Our price is significantly lower than the market price.\n")
                if insight['current_stock'] == '0' or int(insight['current_stock']) < int(insight['restock_threshold']):
                    report_file.write(f"  - Insight: Stock is low or out of stock. Consider reordering.\n")
                report_file.write("\n")
            report_file.write("## Recommendations\n")
            report_file.write("- Adjust prices to be more competitive with market prices\n")
            report_file.write("- Monitor market trends regularly\n")
            report_file.write("- Reorder products that are low or out of stock\n")
    except Exception as e:
        print(f"An error occurred while writing the report: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/analysis.py <csv_file_path>")
        sys.exit(1)
    main(sys.argv[1])
