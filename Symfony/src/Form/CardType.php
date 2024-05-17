<?php

namespace App\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\Extension\Core\Type\NumberType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Validator\Constraints\Length;
use Symfony\Component\Validator\Constraints\NotBlank;
use Symfony\Component\Validator\Constraints\Regex;

class CardType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('dataperson', TextType::class, [
                'label'=>'Imię i nazwisko na karcie',
            ])
            ->add('cvv', IntegerType::class, [
                'constraints' => [
                    new Length(['min'=>3]),
                    new Length(['max' => 4]),
                    new Regex([
                        'pattern' => '/^\d{1,4}$/',
                    ]),
                    new NotBlank(),
                ],
                'label'=>'CVV'
            ])
            ->add('numbercard', TextType::class, [
                'constraints' => [
                    new Length(['min'=>16]),
                    new Length(['max' => 16]),
                    new Regex([
                        'pattern' => '/^\d{1,16}$/',
                    ]),
                    new NotBlank(),
                ],
                'label'=>'Numer karty'
            ])
            ->add('expirationdate', ChoiceType::class, [
                'choices' => $this->getExpirationDateChoices(),
                'label'=> 'Data ważności',
                'constraints'=>[
                    new NotBlank(),
                ]
            ])
        ;
    }

    private function getExpirationDateChoices(): array
    {
        $currentYear = date('Y');
        $choices = [];
        for ($year = $currentYear; $year <= $currentYear + 10; $year++) {
            for ($month = 1; $month <= 12; $month++) {
                $monthLabel = str_pad($month, 2, '0', STR_PAD_LEFT);
                $choices["$year-$monthLabel"] = "$monthLabel/$year";
            }
        }
        return $choices;
    }
    
    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            // Configure your form options here
        ]);
    }
}
