import random
import numpy as np
import time

def encrypt(xytq_minutiae: list, private_key: list) -> list[list]:
    result = []

    for i in range(4):
        a = random.randint(1, 9999)
        b = random.randint(1, 9999)
        c = random.randint(1, 9999)
        d = random.randint(1, 9999)

        e = a * xytq_minutiae[0] + b * xytq_minutiae[1] + c * xytq_minutiae[2] + d * xytq_minutiae[3]

        a_err = a + private_key[0]
        b_err = b + private_key[1]
        c_err = c + private_key[2]
        d_err = d + private_key[3]
        e_err = e + private_key[4]
        result.append([a_err, b_err, c_err, d_err, e_err])

    return result

def decrypt(enc_val: list[list], private_key: list) -> list:
    for i in range(len(enc_val)):
        for j in range(len(enc_val[i])):
            enc_val[i][j] -= private_key[j]

    coefficient_arr = np.array([i[:-1] for i in enc_val])
    constant_arr = np.array([i[-1] for i in enc_val])

    xytq_minutiae = np.linalg.solve(coefficient_arr, constant_arr).tolist()
    xytq_minutiae = [round(val) for val in xytq_minutiae]

    return xytq_minutiae

def main():
    # Read the input file
    input_file_path = 'C:/Users/ankan/Downloads/10_1.jpg.xyt'
    
    minutiae_points = []
    with open(input_file_path, 'r') as file:
        for line in file:
            x, y, t, q = map(int, line.split())
            minutiae_points.append([x, y, t, q])
    
    private_key = [3, 6, 9, 5, 7]
    
    total_encryption_time = 0
    total_decryption_time = 0

    for minutiae in minutiae_points:
        print("Original XYTQ Minutiae:", minutiae)

        start_time = time.time()
        enc_val = encrypt(minutiae, private_key)
        encryption_time = time.time() - start_time
        total_encryption_time += encryption_time
        print("Encrypted XYTQ Minutiae:", enc_val)
        print(f"Encryption Time for this point: {encryption_time:.6f} seconds")

        start_time = time.time()
        dec_minutiae = decrypt(enc_val, private_key)
        decryption_time = time.time() - start_time
        total_decryption_time += decryption_time
        print("Decrypted XYTQ Minutiae:", dec_minutiae)
        print(f"Decryption Time for this point: {decryption_time:.6f} seconds")
        print()

    print(f"Total Encryption Time: {total_encryption_time:.6f} seconds")
    print(f"Total Decryption Time: {total_decryption_time:.6f} seconds")
    print(f"Average Encryption Time per point: {total_encryption_time / len(minutiae_points):.6f} seconds")
    print(f"Average Decryption Time per point: {total_decryption_time / len(minutiae_points):.6f} seconds")

main()
