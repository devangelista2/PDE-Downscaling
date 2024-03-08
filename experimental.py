"""
Visualize max, min, mean on a small region.
"""
# cropped_latitude_id = np.where((latitude > 45.50) & (latitude < 45.74))
# cropped_longitude_id = np.where((longitude > 12.93) & (longitude < 13.17))
# cropped_id = np.intersect1d(cropped_latitude_id, cropped_longitude_id)
# 
# cropped_water_level = water_level[:, cropped_id]
# print(cropped_water_level.shape)
# print(f"Min: {cropped_water_level[0].min()}, Max:{cropped_water_level[0].max()}, Std: {cropped_water_level[0].std()}.")
# 
# plt.plot(cropped_water_level.min(axis=1))
# plt.plot(cropped_water_level.max(axis=1))
# plt.legend(["min", "max"])
# plt.grid()
# plt.show()

"""
Generate Sea Mask (version < 22/02/2024)
"""
# sea_mask = np.zeros((nx, ny))
# l = 1
# coarse_image_mask = coarse_image.copy()[:, :, 0]
# coarse_image_mask[-1, 61:252] = 1
# for i in range(nx):
#     for j in range(ny):
#         sea_above = np.sum(np.abs(coarse_image_mask[:i+1, j])) > 1e-6
#         sea_below = np.sum(np.abs(coarse_image_mask[i:, j])) > 1e-6
#         sea_left = np.sum(np.abs(coarse_image_mask[i, :j+1])) > 1e-6
#         sea_right = np.sum(np.abs(coarse_image_mask[i, j:])) > 1e-6
# 
#         sea_diag_ul = np.sum(np.abs(np.diag(coarse_image_mask[i:, j:])))
#         sea_diag_ur = np.sum(np.abs(np.diag(coarse_image_mask[i:, :j+1])))
#         sea_diag_dl = np.sum(np.abs(np.diag(coarse_image_mask[:i+1, j:])))
#         sea_diag_dr = np.sum(np.abs(np.diag(coarse_image_mask[:i+1, :j+1])))
# 
#         cross = sea_above and sea_below and sea_left and sea_right
#         diags = sea_diag_ul and sea_diag_ur and sea_diag_dl and sea_diag_dr
#         if cross or (np.abs(coarse_image_mask[i, j]) > 1e-6):
#             sea_mask[i, j] = 1