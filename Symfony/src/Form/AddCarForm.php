<?php


namespace App\Form;

use App\Entity\Car;
use phpDocumentor\Reflection\Types\Integer;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Validator\Constraints\GreaterThanOrEqual;

class AddCarForm extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('photopath', TextType::class, [
                'label' => 'Ścieżka do zdjęcia',
                'attr' => [
                    'placeholder' => 'np. https://cdn.pixabay.com/photo/2023/07/17/13/50/baby-snow-leopard-8132690_1280.jpg'
                ],
            ])
            ->add('name', TextType::class, [
                'label' => 'Marka',
                'attr' => [
                    'placeholder' => 'np. BMW'
                ],
            ])
            ->add('model', TextType::class, [
                'label' => 'Model',
                'attr' => [
                    'placeholder' => 'np. M3'
                ],
            ])
            ->add('year_of_production', TextType::class, [
                'label' => 'Rok produkcji',
                'attr' => [
                    'placeholder' => 'np. 2020'
                ],
            ])
            ->add('engine', TextType::class, [
                'label' => 'Silnik',
                'attr' => [
                    'placeholder' => 'np. 4.0 V8'
                ],
            ])
            ->add('power', TextType::class, [
                'label' => 'Moc',
                'attr' => [
                    'placeholder' => 'np. 400'
                ],
            ])
            ->add('acceleration', TextType::class, [
                'label' => 'Przyśpieszenie',
                'attr' => [
                    'placeholder' => 'np. 5.4'
                ],
            ])
            ->add('weight', TextType::class, [
                'label' => 'Masa',
                'attr' => [
                    'placeholder' => 'np. 1920'
                ],
            ])
            ->add('quantity', IntegerType::class, [
                'label' => 'Ilość',
                'attr' => [
                    'min' => 1, //
                ],
                'constraints' => [
                    new GreaterThanOrEqual(1),
                ],
            ])
            ->add('conditioncar', ChoiceType::class, [
                'label' => 'Stan',
                'choices' => [
                    'Nowy' => 'nowy',
                    'Używany' => 'uzywany',
                ],
            ])
            ->add('description', TextareaType::class, [
                'label' => 'Opis',
                'attr' => [
                    'placeholder' => 'np. Fajne auto, fajne wyposażenie.'
                ],
            ])
            ->add('price', IntegerType::class, [
                'label'=> 'Cena',
                'attr' => [
                    'min' => 1,
                ],
                'constraints' => [
                    new GreaterThanOrEqual(1),
                ],
            ]);
    }

    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults([
            'data_class' => Car::class,
        ]);
    }
}


