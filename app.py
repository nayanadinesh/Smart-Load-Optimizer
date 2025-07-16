from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        data = request.get_json()
        capacity = data['capacity']
        items = data['items']

        # Simple Knapsack Algorithm
        n = len(items)
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if items[i-1]['weight'] <= w:
                    dp[i][w] = max(items[i-1]['value'] + dp[i-1][w-items[i-1]['weight']], dp[i-1][w])
                else:
                    dp[i][w] = dp[i-1][w]

        # Track selected items
        selected_items = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_items.append(items[i-1])
                w -= items[i-1]['weight']

        return jsonify({"max_value": dp[n][capacity], "selected_items": selected_items})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
