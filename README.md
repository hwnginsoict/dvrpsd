��#   D V R P S D 

Class Ant():
attributes:
- current node
- candidate node (các đỉnh tiếp có thể ghé)
- visited node
- capacity (giảm dần trên tuyến đường)
- route (ghi lại tuyến đường)
- cost (chi phí cả route)

functions:
- choose_node (chọn node để đi)
- move (đi, cập nhật trạng thái các node)
- local_search

Class ACO()
attributes:
- ants (tập các kiến, đại diện số xe)
- pheromone (ma trận đại diện cho trọng số cạnh, được cập nhật khi kiến đi)
- các tham só như tỉ lệ reward pheromone, độ bay hơi pheromone... (nhiều mà code ngắn nên t để chung)

functions:
- khởi tạo kiến
- update_pheromone (tính toán cost các đường đi và cập nhật ma trận pheromone)

hàm run():
- khởi tạo kiến
- khởi tạo ma trận pheromone, ban đầu bằng 1 hết
- chọn 1 kiến để đi, nhét đường đi vào Ant để Ant tính toán xác suất các tập đỉnh sẽ ghé
- bắt kiến đi, đến khi hết capacity
- kiến tiếp theo
 
 
