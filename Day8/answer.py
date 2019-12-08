def decode_image(image: list, layer_format: list) -> list:
    """
    Return decoded image.
    """
    size_layer = layer_format[0] * layer_format[1]
    num_layers = int(len(image) / size_layer)

    decoded_image = []
    for i in range(size_layer):
        # Only non-transparent pixel
        pixel = [x for x in image[i::size_layer] if x != 2]
        if len(pixel):
            decoded_image.append(pixel[0])
        else:
            decoded_image.append(2)

    return decoded_image


def layer_min_zero(image: list, layer_format: list) -> list:
    """
    Return the layer with minimum number of zeros
    """
    size_layer = layer_format[0] * layer_format[1]
    num_layers = int(len(image) / size_layer)

    min_layer = []
    min_zeros = size_layer + 1

    for start_pos in range(num_layers):
        current_layer = image[start_pos*size_layer : min((start_pos+1)*size_layer, len(image))]
        num_zeros = current_layer.count(0)
        if num_zeros < min_zeros:
            min_layer = current_layer
            min_zeros = num_zeros
    return min_layer


if __name__ == '__main__':
    with open('input.csv', mode='r') as input_file:
        image = [int(x) for x in input_file.read()]

        layer = layer_min_zero(image, [25, 6])
        print("Answer #8.1: ", layer.count(1) * layer.count(2))

        clear_image = decode_image(image, [25, 6])

        for i in range(6):
            print("".join([str(x) if x else '.' for x in clear_image[i*25:(i+1)*25]]))